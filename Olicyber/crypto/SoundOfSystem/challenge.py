#!/bin/env python3

import os
import signal
from Crypto.Cipher import AES

TIMEOUT = 300

seed = os.urandom(16)

def xor(a, b):
    return bytes(x^y for x,y in zip(a,b))

def pad(m):
    if len(m)%48 == 0:
        return m
    return m + bytes([48-len(m)%48])*(48-len(m)%48)

class Hash(object):
    def __init__(self, msg):
        self.seed = seed
        self.msg = pad(msg)

    def hash(self):
        cipher = AES.new(self.seed, AES.MODE_ECB)
        blocks = [self.msg[i:i+16] for i in range(0, len(self.msg), 16)]
        prev = bytes(16)
        res = bytes(16)

        for b in blocks:
            res = xor(xor(prev, res), cipher.decrypt(b))
            prev = b

        return res.hex()



blacklist = [pad(b"show_flag")]

commands = {}
commands[Hash(b"show_flag").hash()] = lambda: os.system("cat flag.txt")
commands[Hash(b"list_files").hash()] = lambda: os.system("ls")
commands[Hash(b"me").hash()] = lambda: os.system("whoami")
commands[Hash(b"where_am_i").hash()] = lambda: os.system("pwd")
commands[Hash(b"what_ive_done").hash()] = lambda: os.system("history")

def handle():
    while True:
        print("Tell me what to do!")
        cmd = input("> ").encode()
        if pad(cmd) in blacklist or len(cmd) > 50:
            print("Command not allowed or too long.")
        else:
            try:
                commands[Hash(cmd).hash()]()
            except:
                print("Unknown error, please try again.")


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
