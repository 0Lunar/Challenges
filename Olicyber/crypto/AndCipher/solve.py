import requests
import threading


API = "http://andcipher.challs.olicyber.it/api/encrypt"
MAX_CICLES = 100

class AndCracker(object):
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._start_threads = threading.Event()
        self.result = b''
    
    @staticmethod
    def getMax(x: bytes, y: bytes) -> bytes:
        return bytes([max(a,b) for a,b in zip(x,y)])


    def proc(self, cicles: int) -> None:
        self._start_threads.wait()
        
        for _ in range(cicles):
            r = requests.get(API)
            resp = r.json()
            resp = bytes.fromhex(resp['encrypted'])
            
            with self._lock:
                self.result = AndCracker.getMax(resp, self.result) or resp


    def run(self, max_cicles: int, threads: int = 16) -> bytes:
        thread_list = []    # type: list[threading.Thread]
        self._start_threads.clear()
        
        for _ in range(threads):
            th = threading.Thread(target=self.proc, args=(max_cicles // threads, ))
            thread_list.append(th)
            th.start()
        
        self._start_threads.set()
        
        for th in thread_list:
            th.join()
            
        return self.result
    

if __name__ == "__main__":
    cracker = AndCracker()
    
    res = cracker.run(150)
    
    print(res.decode())
