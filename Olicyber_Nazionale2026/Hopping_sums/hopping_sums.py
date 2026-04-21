#!/usr/bin/env python3

import os
from random import randrange
from math import gcd

flag = os.getenv('FLAG', 'flag{redacted}').encode()
assert flag.startswith(b'flag{') and flag.endswith(b'}')
flag = flag[5:-1]
l = len(flag)

while 1:
    k = randrange(2, l)
    if gcd(k, l) == 1:
        break

enc = []
for i in [( k * i - 1 ) % l for i in range(l)]:
    enc.append((flag[i] + flag[( i + k ) % l]) & 0xff)

print(bytes(enc).hex())
