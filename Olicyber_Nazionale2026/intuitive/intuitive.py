#!/usr/bin/env python3

import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = os.getenv("FLAG", "flag{test_flag}")

class CBC_MAC:
    def __init__(self):
        self.k = os.urandom(32)
    
    def Mac(self, m):
        cipher = AES.new(self.k, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(m, 16))[-16:]
    
    def Vrfy(self, m, t):
        if len(t) != 32:
            return False
        cipher = AES.new(self.k, AES.MODE_CBC, t[:16])
        return cipher.encrypt(pad(m, 16))[-16:] == t[-16:]

class Oracle:
    def __init__(self):
        self.MAC = CBC_MAC()
        self.seen = set()
    
    def query(self, m, *args):
        t = self.MAC.Mac(m)
        self.seen.add(m)
        return {'ok': 1, 'tag': t.hex()}

    def solve(self, m, t):
        if m not in self.seen and self.MAC.Vrfy(m, t):
            return {'ok': 1, 'flag': FLAG}
        return self.error()
    
    def error(self, *args):
        return {'ok': 0}
    
    def __call__(self, req):
        m, t = None, None
        try:
            req = json.loads(req)
            method = req.get('method')
            assert method in ['query', 'solve']
            m = bytes.fromhex(req.get('m'))
            t = bytes.fromhex(req.get('tag', ''))
        except:
            method = 'error'
        return json.dumps(getattr(self, method)(m, t))


oracle = Oracle()
while 1:
    print(oracle(input('> ')))
