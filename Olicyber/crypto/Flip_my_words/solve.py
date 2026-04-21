from pwn import *
from base64 import b64decode as b64d
from base64 import b64encode as b64e
from Crypto.Util.Padding import pad
import json


def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x^y for x,y in zip(a,b)])


def encrypt(conn: tube, data: bytes) -> tuple[bytes, bytes]:
    conn.sendlineafter(b'!!!\n', b'1')
    conn.sendlineafter(b': ', data)
    ciphertext = conn.recvline().strip().decode().split(": ")[-1]
    iv = conn.recvline().strip().decode().split(": ")[-1]
    
    return b64d(ciphertext), b64d(iv)


def decrypt(conn: tube, ciphertext: bytes, iv: bytes) -> bytes:
    conn.sendlineafter(b'!!!\n', b'2')
    conn.sendlineafter(b': ', b64e(ciphertext))
    conn.sendlineafter(b': ', b64e(iv))
    return conn.recvlines(4)[-1].strip().decode().split(': ')[-1]
    


def evil_iv(iv: bytes, known_plaintext: bytes, target_plaintext: bytes) -> bytes:
    assert len(iv) == 16 and len(known_plaintext) == 16 and len(target_plaintext) == 16
    return xor(xor(known_plaintext, target_plaintext), iv)


def split_block(data: bytes, bs: int) -> list[bytes]:
    return [data[i:i+bs] for i in range(0, len(data), bs)]


if __name__ == '__main__':
    msg = 'Dammi la flaaag!'
    target_plaintext = json.dumps({'admin': True, 'msg': msg}).encode()
    known_plaintext = json.dumps({'admin': False, 'msg': msg}).encode()
    
    with remote("flip.challs.olicyber.it", 10603) as r:
        ciphertext, iv = encrypt(r, msg.encode())
        
        ev_iv = evil_iv(iv, known_plaintext[:16], target_plaintext[:16])
        
        flag = decrypt(r, ciphertext, ev_iv)
        print(flag)