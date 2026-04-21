from pwn import *
import time
from hashlib import sha256
import json
from Crypto.Util.number import long_to_bytes


def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x^y for x,y in zip(a,b)])


if __name__ == '__main__':
    with remote("socket.cryptohack.org", 13372) as r:
        payload = json.dumps({"option": "get_flag"})
        t = time.time()
        r.sendlineafter(b'!\n', payload.encode())
        
        encrypted_flag = r.recvline().strip().decode()
        encrypted_flag = json.loads(encrypted_flag)
        encrypted_flag = bytes.fromhex(encrypted_flag['encrypted_flag'])
        
        key = long_to_bytes(int(t))
        key = hashlib.sha256(key).digest()
        
        print(xor(encrypted_flag, key))