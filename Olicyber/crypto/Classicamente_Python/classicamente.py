import random


def encrypt(data):
    n = 4
    data += "_"*(n - (len(data) % n))
    cols = [data[i::n] for i in range(n)]
    return "".join(cols)


flag = open("../flags.txt", "r").read().strip()
enc = encrypt(flag)
print(enc)
