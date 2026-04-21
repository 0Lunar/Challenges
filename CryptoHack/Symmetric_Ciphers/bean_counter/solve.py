from requests import get as HTTPGet
from pwn import xor


ENC_API = 'https://aes.cryptohack.org/bean_counter/encrypt/'
PNG_SIG = bytes.fromhex('8950 4e47 0d0a 1a0a 0000 000d 4948 4452'.replace(' ', ''))


if __name__ == '__main__':
    res = HTTPGet(ENC_API)
    encrypted = res.json()['encrypted']
    encrypted = bytes.fromhex(encrypted)
    
    blocks = [encrypted[i:i+16] for i in range(0, len(encrypted), 16)]
    iv = xor(blocks[0], PNG_SIG)
    
    with open("flag.png", "wb") as f:
        for block in blocks:
            decrypted = xor(block, iv)
            f.write(decrypted)