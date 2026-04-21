from Crypto.Util.Padding import pad
from pwn import *
import re


target = '''
What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX. Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called "Linux", and many of its users are not aware that it is basically the GNU system, developed by the GNU Project. There really is a Linux, and these people are using it, but it is just a part of the system they use.

Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called "Linux" distributions are really distributions of GNU/Linux.
'''.encode()


def send_cipher(conn: tube, data: bytes) -> bytes:
    conn.sendlineafter(b': ', data.hex().encode())
    out = conn.recvline().decode()
    try:
        return bytes.fromhex(re.findall(r'\'.+\'', out)[0][1:-1])
    except:
        return out.encode()


def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x^y for x,y in zip(a,b)])


def evil_iv(iv: bytes, data: bytes, target: bytes) -> bytes:
    return xor(iv, xor(data, target))


if __name__ == '__main__':
    target = pad(target, 16)
    target_blocks = [target[i:i+16] for i in range(0, len(target), 16)]
    
    iv = target_blocks[-1]
    ciphertext = target_blocks[-1]
    
    with remote("10.45.1.2", 2003) as r:
        for block in range(len(target_blocks) - 1, -1, -1):
            ptx = send_cipher(r, b'\x00' * 16 + iv)
            iv = evil_iv(b'\x00' * 16, ptx, target_blocks[block])
            ciphertext = iv + ciphertext
        
        ptx = send_cipher(r, ciphertext)
        print(ptx)
        
        r.interactive()