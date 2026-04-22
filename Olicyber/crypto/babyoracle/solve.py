from Crypto.Util.number import long_to_bytes, GCD
from pwn import *


if __name__ == '__main__':
    e = 65537
    
    with remote("babyoracle.challs.olicyber.it", 12007) as r:
        n = int(r.recvline().strip().split(b" = ")[-1].decode())
        flag = int(r.recvline().strip().split(b" = ")[-1].decode())
        r.sendlineafter(b': ', b'2')
        out = int(r.recvline().decode())
        
        p = GCD(out ** 65537 - 2, n)
        q = n // p
        
        assert p*q == n
        
        phi = (p-1) * (q-1)
        d = pow(e, -1, phi)
        flag = long_to_bytes(pow(flag, d, n))
        print(flag.decode())