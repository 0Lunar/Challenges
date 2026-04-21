from pwn import *
import json
from sympy.ntheory import discrete_log
import sys

sys.path.append("../")

from Deriving_Symmetric_Keys.decrypt import decrypt_flag


def recv_json(conn: tube):
    data = conn.recvline().decode().strip()
    data = data[data.find(": ") + 2:]
    return json.loads(data)


def get_json_val(data: dict, key: str) -> int:
    return int(data.get(key, '0x00')[2:], 16)


if __name__ == '__main__':
    with remote("socket.cryptohack.org", 13379) as r:
        r.recvline()
        r.sendlineafter(b': ', b'{"supported": ["DH64"]}')
        r.recvline()
        r.sendlineafter(b': ', b'{"chosen": "DH64"}')
        
        dh_alice = recv_json(r)
        dh_bob = recv_json(r)
        enc_flag = recv_json(r)
        
        p = get_json_val(dh_alice, 'p')
        g = get_json_val(dh_alice, 'g')
        A = get_json_val(dh_alice, 'A')
        B = get_json_val(dh_bob, 'B')
        
        iv = enc_flag['iv']
        ciphertext = enc_flag['encrypted_flag']
        
        a = discrete_log(p, A, g)
        K = pow(B, a, p)
        flag = decrypt_flag(K, iv, ciphertext)
        
        print(flag)