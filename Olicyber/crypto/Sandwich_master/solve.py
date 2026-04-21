from pwn import *
from Crypto.Util.Padding import pad
import re


msg = b'Im so good with sandwiches they call me mr Krabs'
iv = b'\x00' * 16


def sign(conn: tube, data: bytes) -> bytes:
    conn.sendlineafter(b'> ', b'1')
    conn.sendlineafter(b': ', data.hex().encode())
    
    out = conn.recvline().strip().decode()
    digest = re.findall(r'\'[\w]+\'', out)[0].strip("\'")
    return bytes.fromhex(digest)


def verify(conn: tube, sign: bytes) -> str:
    conn.sendlineafter(b'> ', b'2')
    conn.sendlineafter(b': ', sign.hex().encode())
    return conn.recvline().strip().decode()


if __name__ == '__main__':
    with remote("sandwichmaster.challs.olicyber.it", 30996) as io:
        data = [msg[i:i+16] for i in range(0, len(msg), 16)]
        status = b'\x00' * 16
        
        for piece in data:
            status = sign(io, xor(piece, status))
        
        flag = verify(io, status)
        print(flag)