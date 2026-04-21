from requests import get as HTTPGet
from datetime import datetime, timedelta
from pwn import xor
from Crypto.Util.Padding import pad


COOKIE_API = 'https://aes.cryptohack.org/flipping_cookie/get_cookie/'
FLAG_API = 'https://aes.cryptohack.org/flipping_cookie/check_admin/%s/%s/'


if __name__ == '__main__':
    cookie = HTTPGet(COOKIE_API)
    cookie = cookie.json()['cookie']
    iv, cookie = bytes.fromhex(cookie[:32]), cookie[32:64]
    
    expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
    tm_cookie = pad(f"admin=False;expiry={expires_at}".encode(), 16)
    
    evil_cookie = pad(b'admin=True;', 16)
    evil_iv = xor(xor(tm_cookie[:16], iv), evil_cookie)
    
    flag = HTTPGet(FLAG_API % (cookie, evil_iv.hex())).json()
    
    if 'flag' in flag:
        print(flag['flag'])