from requests import get as HTTPGet
from Crypto.Util.Padding import pad


ENCRYPT_URL = 'https://aes.cryptohack.org/lazy_cbc/encrypt/{}'
GET_FLAG_URL = 'https://aes.cryptohack.org/lazy_cbc/get_flag/{}'
RECEIVE_URL = 'https://aes.cryptohack.org/lazy_cbc/receive/{}'


class Solver(object):
    @staticmethod
    def encrypt(msg: bytes) -> bytes:
        msg = pad(msg, 16)
        
        resp = HTTPGet(ENCRYPT_URL.format(msg.hex()))
        resp = resp.json()
        
        return bytes.fromhex(resp['ciphertext'])


    @staticmethod
    def get_flag(key: bytes) -> str:
        assert len(key) == 16, "Invalid Key Length"
        
        resp = HTTPGet(GET_FLAG_URL.format(key.hex()))
        resp = resp.json()
        ky = list(resp.keys())[0]
        
        return resp[ky]
    
    
    @staticmethod
    def receive(ciphertext: bytes) -> str:
        assert len(ciphertext) % 16 == 0, "Invalid Ciphertext length"
        
        resp = HTTPGet(RECEIVE_URL.format(ciphertext.hex()))
        resp = resp.json()
        ky = list(resp.keys())[0]
        
        return resp[ky]
    
    
    @staticmethod
    def xor(a: bytes, b: bytes) -> bytes:
        return bytes([x^y for x,y in zip(a,b)])
    
    
if __name__ == '__main__':
    c0 = Solver.encrypt(b'Q' * 16)[:16]
    c1 = Solver.encrypt(b'Q' * 16 + c0)[16:32]
    key = Solver.receive(c1)
    
    key = bytes.fromhex(key.split(': ')[-1].strip())
    flag = bytes.fromhex(Solver.get_flag(key)).decode()
    
    print(flag)