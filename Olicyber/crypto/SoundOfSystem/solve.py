from pwn import *


def pad(m):
    if len(m)%48 == 0:
        return m
    return m + bytes([48-len(m)%48])*(48-len(m)%48)


if __name__ == '__main__':
    pd_msg = pad(b'show_flag')
    
    with remote("soundofsystem.challs.olicyber.it", 15000) as r:
        r.sendlineafter(b'> ', b'\x27' * 16 + b'show_flag' + b'\x27' * 23)
        r.interactive()