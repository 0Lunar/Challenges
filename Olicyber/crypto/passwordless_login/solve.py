import requests
import json
import re


class Solver(object):
    def __init__(self) -> None:
        self.API = 'http://passwordlesslogin.challs.olicyber.it/execute'
    
    def solve(self) -> str:
        # Register
        header = {
            "Content-Type": "application/json"    
        }
        payload = {
            "fn": "register",
            "inputs": ["Am1234567890123456ministratore"]
        }
        
        r = requests.post(self.API, headers=header, data=json.dumps(payload))
        token = bytes.fromhex(r.json()['result'])
        token = token[:16] + token[32:]
        
        payload['fn'] = 'login'
        payload['inputs'] = [token.hex()]
        
        r = requests.post(self.API, headers=header, data=json.dumps(payload))
        res = r.json()['result']
        return re.findall(r'ITASEC{.+}', res)[0]


if __name__ == '__main__':
    s = Solver()
    flag = s.solve()
    print(flag)