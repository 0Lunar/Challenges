from hashlib import sha256
import os
import multiprocessing
from pwn import *
import time as time_time
from colorama import Fore


class PoW(object):
    def __init__(self) -> None:
        self._lock = multiprocessing.Lock()
        self.found = multiprocessing.Event()
        self.secret = multiprocessing.Queue(2)
        self.expired = multiprocessing.Event()
        self.hash_dict = None
    
    
    def _findPow(self, lsb: bytes) -> None: 
        t = time_time.time()
        
        while not self.found.is_set():
            if time_time.time() - t > 50:
                with self._lock:
                    self.expired.set()
                    self.found.set()
                    return
            
            res = os.urandom(4)

            if sha256(res).digest().startswith(lsb):
                with self._lock:
                    self.secret.put(res)
                    self.secret.put(time_time.time() - t)
                    self.found.set()
                    break
            

    def _makeDict(self, timeout: float | int) -> None:
        t = time_time.time()
        local_hash = {}
                
        while time_time.time() - t <= timeout:
            rnd = os.urandom(4)
            hash_obj = sha256(rnd).digest()[:3]
            hash_obj = int.from_bytes(hash_obj, 'big')
            
            if hash_obj not in local_hash:
                local_hash[hash_obj] = rnd

        with self._lock:
            self.hash_dict.update(local_hash)
        
        log.success(f"Shared dict updated")


    def makeDict(self, procs: int = 16, timeout: float | int = 60.0) -> None:
        process_list = []
        self.hash_dict = multiprocessing.Manager().dict()
        
        for pr in range(procs):
            process = multiprocessing.Process(target=self._makeDict, args=(timeout,))
            process_list.append(process)
            process.start()
            
        t = time_time.time()
        while time_time.time() - t <= timeout:
            print(f"[{Fore.BLUE}*{Fore.RESET}] Time: {time_time.time() - t:.02f} / {timeout}", end="\r")
        print()
        
        log.info("Waiting processes to exit...")
        for process in process_list:
            process.join()
            log.info(f"{process.pid} Exited")

        log.info("Copying shared dict to local dict...")
        hash_dict = {}
        hash_dict.update(self.hash_dict)
        self.hash_dict = hash_dict
        log.success("Done")

        
    def findPow(self, lsb: bytes, procs: int = 16) -> tuple[bytes, float]:
        if self.hash_dict is not None and int.from_bytes(lsb, 'big') in self.hash_dict:
            return (self.hash_dict[int.from_bytes(lsb, 'big')], 0)
        
        self.found.clear()
        self.expired.clear()
        
        process_list = []
        for pr in range(procs):
            process = multiprocessing.Process(target=self._findPow, args=(lsb,))
            process_list.append(process)
            process.start()
        
        self.found.wait()
        
        for process in process_list:
            process.join()
        
        if self.expired.is_set():
            return (b'', 0)
        
        return (self.secret.get(), self.secret.get())
            

if __name__ == "__main__":
    pow = PoW()
    
    log.info("Making hash list...")
    pow.makeDict(12, 10)
    log.info(f"Hash list size: {len(pow.hash_dict.keys())} items")
    
    conn = remote("pow.challs.olicyber.it", 12209)
    
    while True:
        msg = conn.recvline()
        
        if not msg.startswith(b'Give me x so that sha256(bytes.fromhex(x)) starts with'):
            print(msg)
            break
        
        secret = msg.decode().strip().split(" ")[-1]
        log.info(f"Searching PoW for hash {secret}")
        
        if secret in pow.hash_dict:
            log.success("Hash in dictionary!!!")
        
        secret, time = pow.findPow(bytes.fromhex(secret), 12)
        
        if secret != b'':
            log.success(f"PoW found: {secret.hex()}")
            log.info("Time: {:.02f} s".format(time))
            conn.sendline(secret.hex().encode())
        
        else:
            log.error(f"Expired time")
            conn.close()
            break
    
    conn.interactive()
