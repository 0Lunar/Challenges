import sympy.ntheory
from Crypto.Util.number import long_to_bytes
import json


if __name__ == "__main__":
    a = 288260533169915
    p = 1007621497415251
    
    with open("output.txt", "rt") as f:
        data = json.load(f)
        
    out = ''
        
    for n in data:
        try:
            sympy.ntheory.discrete_log(p, n, a)
            out += '1'
        except:
            out += '0'
        
    out = int(out, 2)
    out = long_to_bytes(out)
    
    print(out.decode())