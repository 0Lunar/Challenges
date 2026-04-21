from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad
from pwn import *
import json
import os


def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])


with remote("intuitive.challs.nazionale.olicyber.it", 38097) as r:
    r.sendlineafter(b'> ', json.dumps({"method": "query", "m": "00" * 16}).encode())
    resp = r.recvline().strip()
    resp = bytes.fromhex(json.loads(resp)['tag'])
    
    iv = resp[:16]
    msg = resp[16:]
    
    r.sendlineafter(b'> ', json.dumps({"method": "solve", "m": iv.hex(), "tag": "00" * 16 + msg.hex()}).encode())
    r.interactive()