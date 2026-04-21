from pwn import *
from base64 import b64encode, b64decode


if __name__ == '__main__':
    conn = remote("pwntools-tutorial.chals.beginner.havce.it", 31337)
    
    for _ in range(60):
        chall = conn.recvline()
        conn.recvuntil(b'> ')
        
        if chall.startswith(b'Converti questo numero da esadecimale a decimale:'):
            num = int(chall.decode().split(": ")[-1].strip()[2:], 16)
            conn.sendline(str(num).encode())
        
        elif chall.startswith(b'Inverti questa stringa:'):
            st = chall.decode().split(": ")[-1][::-1].strip()
            conn.sendline(st.encode())
            
        elif chall.startswith(b'Codifica in Base64 la seguente stringa: '):
            st = chall.decode().split(": ")[-1].strip()
            encoded = b64encode(st.encode())
            conn.sendline(encoded)
            
        elif chall.startswith(b'Converti questo numero in esadecimale (includi 0x davanti):'):
            num = int(chall.decode().split(": ")[-1].strip())
            res = hex(num)
            conn.sendline(res.encode())
            
        elif chall.startswith(b'Decodifica questa stringa Base64:'):
            encoded = chall.decode().split(': ')[-1]
            decoded = b64decode(encoded.encode())
            conn.sendline(decoded)
        
        else:
            print(chall)
            conn.interactive()
            
        conn.recvline()
    
    print(conn.recvline().decode().strip())
    conn.close()