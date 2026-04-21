def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    out = b''
    key_x = 0
    
    for x in range(len(ciphertext)):
        if ciphertext[x] >= b'A'[0] and ciphertext[x] <= b'Z'[0]:
            out += bytes([(((ciphertext[x] - 65) - (key[key_x] - 65)) % 26) + 65])
            key_x = (key_x + 1) % len(key)
        
        elif ciphertext[x] >= b'a'[0] and ciphertext[x] <= b'z'[0]:
            out += bytes([(((ciphertext[x] - 97) - (key[key_x] - 97)) % 26) + 97])
            key_x = (key_x + 1) % len(key)
        
        else:
            out += bytes([ciphertext[x]])
        
    return out


def detect_key(ciphertext: bytes, plaintext: bytes) -> bytes:
    out = b''
    pl_x = 0
    
    for x in range(len(ciphertext)):
        if ciphertext[x] >= b'A'[0] and ciphertext[x] <= b'Z'[0]:
            out += bytes([(((ciphertext[x] - 65) - (plaintext[pl_x] - 65)) % 26) + 65])
        
        elif ciphertext[x] >= b'a'[0] and ciphertext[x] <= b'z'[0]:
            out += bytes([(((ciphertext[x] - 97) - (plaintext[pl_x] - 97)) % 26) + 97])


        pl_x = (pl_x + 1) % len(plaintext)

    return out


key = b'szopnhrbdtbechmapzubrruziakjiqfvwfznz'

with open("ciphertext.txt", "rb") as f:
    data = f.read().strip()

flag = decrypt(data, key)
print(flag.decode())