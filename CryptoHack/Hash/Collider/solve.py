from pwn import *
import json


if __name__ == '__main__':
    with open('dt1', 'rb') as f:
        dt1 = f.read()
        
    with open('dt2', 'rb') as f:
        dt2 = f.read()
        
    payload1 = {"document": dt1.hex()}
    payload2 = {"document": dt2.hex()}
    
    with remote("socket.cryptohack.org", 13389) as io:
        io.recvline()
        io.sendline(json.dumps(payload1).encode())
        io.recvline()
        io.sendline(json.dumps(payload2).encode())
        io.interactive()