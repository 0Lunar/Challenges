from pwn import *               # type: ignore
from randcrack import RandCrack
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes


def getRandBits(conn: tubes.sock.sock) -> list[int]:
    conn.sendlineafter(b'> ', b'1')
    conn.sendlineafter(b': ', b'test')
    ciphertext = conn.recvline()
    key = conn.recvline().strip().split(b": ")[-1].decode()
    iv = conn.recvline().strip().split(b": ")[-1].decode()
    
    key = bytes.fromhex(key)
    iv = bytes.fromhex(iv)
    
    bits = key + iv
    bits = [int.from_bytes(bits[i:i+4], 'little') for i in range(0, len(bits), 4)]
    
    return bits


def getEncodedFlag(conn: tubes.sock.sock) -> bytes:
    conn.sendlineafter(b'> ', b'3')
    ciphertext = conn.recvline().split(b': ')[-1][:-1].decode()
    ciphertext = bytes.fromhex(ciphertext)
    
    return ciphertext


def main() -> None:
    cracker = RandCrack()
    bits = []
    
    conn = remote("lazy-platform.challs.olicyber.it", 16004)
        
    for i in range(52):
        res = getRandBits(conn)
        log.info(f"Recived {(i+1) * 12} bits: {res[:2]}...")
        bits += res
    
            
    for b in bits:
        cracker.submit(b)
    
    
    key = long_to_bytes(cracker.predict_getrandbits(32*8))[::-1]
    iv = long_to_bytes(cracker.predict_getrandbits(16*8))[::-1]
            
    log.info(f"AES Key: {key.hex()}")
    log.info(f"AES Iv: {iv.hex()}")
        
    flag = getEncodedFlag(conn)
    
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    flag = unpad(cipher.decrypt(flag), AES.block_size)
    
    log.success(f"Flag found: {flag.decode()}")


if __name__ == "__main__":
    main()
