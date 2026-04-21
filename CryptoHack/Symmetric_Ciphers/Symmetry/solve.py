from requests import get as HTTPGet


ENC_FLAG_API = 'https://aes.cryptohack.org/symmetry/encrypt_flag'
ENC_API = 'https://aes.cryptohack.org/symmetry/encrypt/{}/{}/'


class CryptoInterface(object):
    @staticmethod
    def get_encrypted_flag() -> bytes:
        return bytes.fromhex(HTTPGet(ENC_FLAG_API).json()['ciphertext'])

    
    @staticmethod
    def encrypt(plaintext: bytes, iv: bytes) -> bytes:
        assert len(iv) == 16, "IV length must be 16"
        
        return bytes.fromhex(HTTPGet(ENC_API.format(plaintext.hex(), iv.hex())).json()['ciphertext'])
    
    
    @staticmethod
    def xor(a: bytes, b: bytes):
        lna = len(a)
        lnb = len(b)
        return bytes([a[x % lna] ^ b[x % lnb] for x in range(max(lna, lnb))])


if __name__ == '__main__':
    flag = CryptoInterface.get_encrypted_flag()
    iv, flag = flag[:16], flag[16:]
    
    flags = [flag[i:i+16] for i in range(0, len(flag), 16)]
    out = b''
    
    for flag in flags:
        iv = CryptoInterface.encrypt(b'\x00' * 16, iv)
        out += CryptoInterface.xor(flag, iv)
        
    print(out)