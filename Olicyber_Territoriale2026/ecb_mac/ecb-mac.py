#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

flag = os.getenv("FLAG", "flag{example_flag}")
assert flag.startswith("flag{") and flag.endswith("}")

def xor(a,b):
    return bytes(x ^ y for x, y in zip(a, b))

def rotate_left(block, i):
    return block[i:] + block[:i]

def ecb_mac(key, msg):
    cipher = AES.new(key, AES.MODE_ECB)
    mac = b'\x00' * 16
    blocks = [msg[i:i+16] for i in range(0, len(msg), 16)]
    for i, block in enumerate(blocks):
        mac = xor(mac, rotate_left(cipher.encrypt(rotate_left(block, i)), i))

    return mac

target_msg = "Questo è un messaggio a caso lungo esattamente 16 blocchi. 16 blocchi sono 16x16 = 256 bytes cioè 2048 bits. Non è facile arrivare ad una lunghezza del genere, dopo un po' finiscono le idee su cosa scrivere. Comunque dovremmo aver quasi finito, ciao!!!!"
target_msg = target_msg.encode()
assert len(target_msg) == 256

if __name__ == "__main__":
    print("Pensi di riuscire a rompere il mio ECB-MAC in un solo tentativo?")
    key = os.urandom(16)
    msg = bytes.fromhex(input("Manda il messaggio (in hex): "))
    if msg == target_msg:
        print("Troppo facile")
        exit()
    if len(msg) > 16*16 or len(msg) % 16 != 0:
        print("Errore nella lunghezza del messaggio!")
        exit()
    mac = ecb_mac(key, msg)

    print(f"MAC: {mac.hex()}")

    guess = bytes.fromhex(input("Manda il MAC del messaggio target (in hex): "))
    if guess == ecb_mac(key, target_msg):
        print(flag)
    else:
        print("Sbagliato! Riprova la prossima volta!")
    



