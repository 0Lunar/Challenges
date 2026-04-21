"""
msg_size = 197
msg_size_padded = 208


block[0] = b'Bob:' + padding(11)
block[1:13] = fake_padding
block[14:26] = encrypted_msg
block[27] = padding(16)
"""
from pwn import *
import base64


def get_blocks(conn: tube, padding_size: int = 208) -> list[bytes]:
    conn.sendlineafter(b': ', b'A'*(22 + padding_size))
    out = base64.b64decode(conn.recvlines(2)[1])
    conn.sendlineafter(b'1\n', b'1')
    
    return [out[i:i+16] for i in range(0, len(out), 16)][:-1]


def calc(conn: tube, msg: bytes, alph: str) -> dict:
    dc : dict = {}
    
    for x in alph:
        conn.sendlineafter(b': ', b'A' * 11 + b'A' * (15 - len(msg)) + msg + x.encode())
        out = base64.b64decode(conn.recvlines(2)[1])
        out = out[16:32]
        
        conn.sendlineafter(b'1\n', b'1')
            
        dc[out] = x
    
    return dc


if __name__ == '__main__':
    pad_sz = 207
    msg = b''
    alph = 'abcdefghijklmnopqrstuvwxyz1234567890_-?!{} '
    
    with remote("bob.challs.olicyber.it", 10602) as r:
        dc = calc(r, msg, alph)
        block = get_blocks(r, pad_sz)[13]
        
        print('Block:', block.hex())
        
        for c in dc:
            print(dc[c], c.hex())