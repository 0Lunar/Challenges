#!/bin/env python3
from pwn import remote, context


def solve() -> bytes:
    res = ''
    
    for idxs in range(1, len(mosse) + 1):
        while stato[mosse[idxs-1][0]] != 5:
            for idx in range(len(mosse[idxs-1])):
                stato[mosse[idxs-1][idx]] += 1
            
            res += str(idxs) + ' '
    
    print(res)
    return res.encode()
            

with remote("test1.challs.olicyber.it", 15004) as r:
    context.log_level = 'info'
    r.recvlines(20)

    livello = r.recvline().decode()
    while livello.startswith("Livello"):
        stato = [int(_) for _ in r.recvline(False).decode().split()]
        mosse = []
        while True:
            s = r.recvline(False).decode()
            if s == "":
                break
            mosse.append(["ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(_) for _ in s.split()])
        res = solve()
        r.sendline(res)
        r.recvlines(2)
        livello = r.recvline().decode()

    print(livello)
    r.interactive()