#nc 10.45.1.2 2002
from pwn import *


if __name__ == '__main__':
    with remote("10.45.1.2", 2002) as r:
        flag = r.recvline().decode().strip()
        flag = bytes.fromhex(flag).decode()
        print(flag)
        
        r.interactive()