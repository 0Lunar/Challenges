#!/usr/bin/env python3
import os
from Crypto.Util.Padding import pad, unpad
import multiprocessing as mp


flag = os.getenv('FLAG', 'flag{redacted}')
ROUNDS = 10


# Semplice xor
def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x^y for x,y in zip(a,b)])


# a + b & 128 bit
def add(a: bytes, b: bytes) -> bytes:
    return int.to_bytes((int.from_bytes(a, 'big') + int.from_bytes(b, 'big')) & ((1 << 128) - 1), 16, 'big')


# Inverso di add
def sub(a: bytes, b: bytes) -> bytes:
    return int.to_bytes((int.from_bytes(a, 'big') - int.from_bytes(b, 'big')) & ((1 << 128) - 1), 16, 'big')


# (x << n | x >> 128 - n) & 128 bit
def rol(x: bytes, n: int) -> bytes:
   return int.to_bytes(((int.from_bytes(x, 'big') << n) | (int.from_bytes(x, 'big') >> (128 - n))) & ((1 << 128) -1), 16, 'big')


# Unrol di rol
def unrol(x: bytes, n: int) -> bytes:
    return int.to_bytes(((int.from_bytes(x, 'big') >> n) | (int.from_bytes(x, 'big') << (128 - n))) & ((1 << 128) -1), 16, 'big')
    

# Wrapper per rol
def ror(x: bytes, n: int) -> bytes:
   return rol(x, 128 - n)


# Wrapper per unrol
def unror(x: bytes, n: int) -> bytes:
    return unrol(x, 128 - n)


# Generate seed list
# [n, n^2, n^4, n^8, ...] % n
def prng(n: int, seed: int, iterations: int) -> list[int]:
  numbers = []
  for _ in range(iterations):
    seed = (seed ** 2) % n
    numbers.append(seed)
  return numbers


def encrypt_block(key: bytes, block: bytes) -> bytes:
    # Check key/block size
    assert len(key) == 32
    assert len(block) == 32
    
    # Split key in half
    k2, k1 = key[:16], key[16:]
    
    # Split block in half
    b1, b2 = block[:16], block[16:]
    
    # b2 = (b1 + b2) ^ k2
    # b1 = ror(b1, 31) ^ k1
    for r in range(ROUNDS):
        b2 = add(b1, b2)
        b2 = xor(b2, k2)
        b1 = ror(b1, 31)
        b1 = xor(b1, k1)
    return b1 + b2
    
    
def decrypt_block(key: bytes, block: bytes) -> bytes:
    # Check key/block size
    assert len(key) == 32
    assert len(block) == 32
    
    # Split key in half
    k2, k1 = key[:16], key[16:]
    
    # Split block in half
    b1, b2 = block[:16], block[16:]
    
    for r in range(ROUNDS):
        b1 = xor(b1, k1)
        b1 = unror(b1, 31)
        b2 = xor(b2, k2)
        b2 = sub(b2, b1)
    return b1 + b2


def encrypt(key: bytes, msg: bytes) -> bytes:
    padded = pad(msg, 32)
    encrypted = b''
    
    for i in range(len(padded) // 32 - 1):
        encrypted += encrypt_block(key, padded[32*i:32*i+32])
        
    return encrypted


def decrypt(key: bytes, enc: bytes) -> bytes:
    assert len(key) == 32, "Invalid length"
    
    decrypted = b''
    
    for i in range(len(enc) // 32):
        decrypted += decrypt_block(key, enc[32*i : 32*i + 32])
    
    try:
        return unpad(decrypted, 32)
    except:
        return decrypted
    

"""
def child_proc(enc: bytes, n: int, start: int, end: int) -> None:
    for seed in range(start, end):
        key = int.to_bytes(prng(n, seed, 10)[-1], 2048//8, 'big')[16:16+32]        
        dec = decrypt(key, enc)
        
        if dec != b'' and dec.startswith(b'flag'):
            print(seed, dec)


if __name__ == "__main__":
    n = 28087460813174486059034414551240249788023923756050759856308458322681826441049323969972913966894664237696959566808290405727732350393345948504891177099061573610135163058514828369697643042666005384521714256517991315882984306833419862539867692692716617074207808746659453884745255262698130584357835902471931699817647567728572688737596486809390298684489842424609146835280833441401592250553573771844222020121038815882223862298294665424093073182955018154044019485219838690648719703150807518955331895641688078886409605207252562543480484708396495057837290115243183136250323437141077720724973892227190571167633700090224634792701
    enc = bytes.fromhex("f12d1653bd9d4c3196860b77ffbe1862c67aca872cf2f793b97678f2478c6b7a9859372ac514d815a28a2657060b64777a272ef12c2c670f908266e4df0e8243")
    
    proclist = []
    
    for seed in range(0, 1_000_000, 100_000):
        proc = mp.Process(target=child_proc, args=(enc, n, seed, seed + 100_000))
        proclist.append(proc)
        
        proc.start()
    
    
    for proc in proclist:
        proc.join()
"""

if __name__ == "__main__":
    seed = 488348
    n = 28087460813174486059034414551240249788023923756050759856308458322681826441049323969972913966894664237696959566808290405727732350393345948504891177099061573610135163058514828369697643042666005384521714256517991315882984306833419862539867692692716617074207808746659453884745255262698130584357835902471931699817647567728572688737596486809390298684489842424609146835280833441401592250553573771844222020121038815882223862298294665424093073182955018154044019485219838690648719703150807518955331895641688078886409605207252562543480484708396495057837290115243183136250323437141077720724973892227190571167633700090224634792701
    enc = bytes.fromhex("f12d1653bd9d4c3196860b77ffbe1862c67aca872cf2f793b97678f2478c6b7a9859372ac514d815a28a2657060b64777a272ef12c2c670f908266e4df0e8243")
    
    key = int.to_bytes(prng(n, seed, 10)[-1], 2048//8, 'big')[16:16+32]
    dec = decrypt(key, enc)
    
    print(dec.decode())
