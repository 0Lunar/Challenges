import requests
import base64
import json


class Solver(object):
    def __init__(self) -> None:
        self.s = requests.Session()
        self.API = "http://flipper-equation.challs.olicyber.it/"
    
    @staticmethod
    def xor(a: bytes, b: bytes) -> bytes:
        return bytes([x^y for x,y in zip(a,b)])
    
    def get_new_cookie(self) -> None:
        self.s.cookies.clear()
        self.s.get(self.API)
        
    def save_session(self) -> str:
        r = self.s.get(f'{self.API}/save_session')
        return r.json()['token']
    
    def solve_equation(self) -> None:
        cookie = self.s.cookies.get("session")
        cookie = cookie.split(".")[0]
        solve = json.loads(base64.b64decode(cookie + '=' * (len(cookie) % 4)).decode())['solution']
        solve = json.dumps({"solution": solve})
        header = {
            "Content-Type": "application/json"
        }
        
        self.s.post(f'{self.API}/solve', headers=header, data=solve)
    
    def craft_payload(self, token: str) -> str:
        # token: ;pts=01000000000
        cookie = self.s.cookies.get("session")
        cookie = cookie.split(".")[0]
        solves = json.loads(base64.b64decode(cookie + '=' * (len(cookie) % 4)).decode()).get('points', 0)
        
        tk = base64.b64decode(token)
        iv = tk[:16]
        ciphertext = tk[16:]
        
        new_iv = self.xor(f';pts={1_000_000_000:011d}'.encode(), f';pts={solves:011d}'.encode())
        new_iv = self.xor(new_iv, iv)
        exp = new_iv + ciphertext
                
        return base64.b64encode(exp).decode()

    def solve(self) -> str:
        self.get_new_cookie()
        self.solve_equation()
        token = self.save_session()
        exploit = s.craft_payload(token)
        return exploit
    
if __name__ == '__main__':
    s = Solver()
    exploit = s.solve()
    print(f'Token: {exploit}')