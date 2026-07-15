import os
from pwn import xor


def custom_xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])


if __name__ == '__main__':
    stats = os.stat('./ch3.bmp')
    file_size = stats.st_size
    
    magic_bytes = b'\x42\x4d' + file_size.to_bytes(4, 'little') + b'\x00' * 4 + b'\x36\x00\x00\x00'
    
    with open("ch3.bmp", "rb") as f:
        data = f.read()
        
    key = bytes.fromhex('66616c6c656e')
    print(key.hex())
    data = xor(data, key)
    
    with open("ch3_new.bmp", "wb") as f:
        f.write(data)