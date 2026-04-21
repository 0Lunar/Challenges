from pwn import *
import json
import sys
import random

sys.path.append("../")

from Deriving_Symmetric_Keys.decrypt import decrypt_flag
from Deriving_Symmetric_Keys.source import encrypt_flag


def parse_json(data: str):
    data = data[data.find(": ") + 2:]
    return json.loads(data)


def get_json_val(data: dict, key: str) -> int:
    return int(data.get(key, '0x00')[2:], 16)


if __name__ == '__main__':
    with remote("socket.cryptohack.org", 13371) as r:
        alice_data = r.recvline().decode().strip()
        alice_data = parse_json(alice_data)

        p = get_json_val(alice_data, 'p')
        g = get_json_val(alice_data, 'g')
        alice_A = get_json_val(alice_data, 'A')
        
        alice_evil_a = random.getrandbits(
            p.bit_length() - 1
        )
        
        alice_evil_A = pow(g, alice_evil_a, p)
        
        alice_evil_data = alice_data
        alice_evil_data['A'] = hex(alice_evil_A)
        alice_evil_data_json = json.dumps(alice_evil_data)
        
        r.sendlineafter(b': ', alice_evil_data_json.encode())
        
        bob_data = r.recvline().decode().strip()
        bob_data = parse_json(bob_data)
        
        bob_B = get_json_val(alice_data, 'B')
        
        bob_evil_b = random.getrandbits(
            p.bit_length() - 1
        )
        
        bob_evil_B = pow(g, bob_evil_b, p)
        
        bob_evil_data = {"B": hex(bob_evil_B)}
        bob_evil_data_json = json.dumps(bob_evil_data)
        
        r.sendlineafter(b': ', bob_evil_data_json.encode())
        
        encrypted_data = r.recvline().decode().strip()
        encrypted_data = parse_json(encrypted_data)
        
        iv = encrypted_data['iv']
        ciphertext = encrypted_data['encrypted_flag']
        
        Ka = pow(alice_A, bob_evil_b, p)
        flag = decrypt_flag(Ka, iv, ciphertext)
        
        print(flag)
        
        r.interactive()