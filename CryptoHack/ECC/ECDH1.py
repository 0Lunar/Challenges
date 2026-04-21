from typing import Any, Iterable
from hashlib import sha1


class Point(list):
    def __init__(self, point: Iterable[int]) -> None:
        self.point = point
        super().append(point[0])
        super().append(point[1])
        
    
    def __getitem__(self, name: str | int) -> Any:
        if type(name) is str:
            if name.lower() == 'x':
                return self.point[0]

            elif name.lower() == 'y':
                return self.point[1]
            
            else:
                return None
        
        return super().__getitem__(name)
    
    
    def __getattribute__(self, name: str) -> Any:                
        if name.lower() == 'x':
            return self.point[0]
    
        elif name.lower() == 'y':
            return self.point[1]
        
        return super().__getattribute__(name)
    

class ECC(object):
    def __init__(self, a: int, b: int, m: int) -> None:
        self.a = a
        self.b = b
        self.m = m
    
    def calc(self, x) -> int:
        return (x**3 + self.a*x + self.b) % self.m
    


class ScalarMult(object):
    def __init__(self, p: Point, ecc: ECC) -> None:
        self.p = p
        self.ecc = ecc


    def _inv_mod(self, n: int, p: int) -> int:
        return pow(n, -1, p)


    def _point_add(self, P: Point, Q: Point, ecc: ECC):
        x1, y1 = P
        x2, y2 = Q
        
        if P == Q:
            lam = ((3 * x1 ** 2 + ecc.a) * self._inv_mod(2 * y1, ecc.m)) % ecc.m
        else:
            lam = ((y2 - y1) * self._inv_mod(x2 - x1, ecc.m)) % ecc.m
            
        x3 = (lam ** 2 - x1 - x2) % ecc.m
        y3 = (lam * (x1 - x3) - y1) % ecc.m
        
        return (x3, y3)


    def __mul__(self, x: int) -> Point:
        assert type(x) is int or (type(x) is float and x.is_integer()), 'Invalid number'

        Q = self.p
        R = None
        
        while x > 0:
            if x % 2 == 1:
                if R is None:
                    R = Q
                
                elif type(R) is Point:
                    R = Point(self._point_add(R, Q, self.ecc))
            
            Q = Point(self._point_add(Q, Q, self.ecc))
            x //= 2
        
        if R is not None:
            return R
    
        return Point((0,0))
            


if __name__ == '__main__':
    ecc = ECC(497, 1768, 9739)
    G = Point([1804,5368])
    Qa = Point([815,3190])
    Nb = 1829

    sm = ScalarMult(Qa, ecc)
    res = sm*Nb 

    x = str(res.x).encode()
    key = sha1(x).hexdigest()

    print('crypto{' + key + '}')
