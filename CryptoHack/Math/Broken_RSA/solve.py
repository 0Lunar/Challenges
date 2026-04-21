from sympy.ntheory import sqrt_mod, isprime
from sympy import legendre_symbol
import io
from Crypto.Util.number import long_to_bytes


def parse_line(f: io.TextIOWrapper) -> int:
    return int(f.readline().strip().split(' = ')[-1])


def solver(ct: int, e: int, p: int) -> list:
    if not legendre_symbol(ct, p) or e == 1:
        return [ct]
    
    nums = sqrt_mod(ct, p, all_roots=True)
    out = []
    
    if type(nums) != list:
        nums = [nums]
    
    for n in nums:
        if legendre_symbol(n, p) == 1:
            out.append(n)
        
    return out


def checkText(data: bytes) -> bool:
    for d in data:
        if d < 32 or d > 127:
            return False
        
    return True
    

if __name__ == "__main__":
    with open("broken_rsa.txt", "rt") as f:
        n = parse_line(f)
        e = parse_line(f)
        ct = parse_line(f)
            
    
    out = [ct]
    
    for _ in range(4):
        tmp = []
        
        for nm in out:
            tmp += solver(nm, e, n)
        
        if out == tmp:
            break
                
        out = tmp
        
    for n in out:
        n = long_to_bytes(n)
        
        if checkText(n):
            print(n.decode())
