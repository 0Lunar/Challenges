"""
N = p * q
c1 = (2 * p + 3 * q) ** e1 mod N
c2 = (5 * p + 7 * q) ** e2 mod N
"""
from io import TextIOWrapper
from sympy import gcd


def parse_line(f: TextIOWrapper) -> str:
    return f.readline().strip().split(' = ')[-1]


if __name__ == "__main__":
    with open("output.txt", "rt") as f:
        N = int(parse_line(f))
        e1 = int(parse_line(f))
        e2 = int(parse_line(f))
        c1 = int(parse_line(f))
        c2 = int(parse_line(f))
        
    
    q = gcd((pow(2, -e1 * e2, N) * pow(c1, e2, N)) - (pow(5, -e1 * e2, N) * pow(c2, e1, N)), N)
    p = N // q
    
    print('crypto{' + str(p) + ', ' + str(q) + '}')