"""
L'algoritmo di Tonelli-Shanks serve a calcolare in mod computazionalmente veloce il residuo quadratico di r ^ 2 = n mod p 
dove p è un numero primo dispari

Questo algoritmo viene usato anche per trovare dei punti nelle curve ellittiche con un valore x

y^2 = x^3 + ax + b è una curva ellittica

Se generiamo un valore casuale in x e calcoliamo n = x^3 + ax + b allora per trovare un punto sulla curva ellittica con valore x dovremo risolvere y^2 = n 

Perchè una soluzione esista, n deve essere un residuo quadratico.
Questo può essere determinato dal criterio di Eulero
"""

from Crypto.Util.number import isPrime


class TonelliShanks(object):
    def __init__(self, n: int, p: int) -> None:
        if p < 3 or not isPrime(p):
            raise RuntimeError("P deve essere un numero primo > 2")

        self.n = n
        self.p = p
        self.r = 0
        
        if TonelliShanks.criterio_eulero(self.n, self.p) == -1:
            raise RuntimeError("N non e' un residuo quadratico")


    @staticmethod
    def criterio_eulero(n, p) -> int:
        if n % p == 0:
            return False

        return pow(n, (p - 1) // 2, p)


    def run(self) -> int | tuple:
        if self.p % 4 == 3:
            return pow(n, (self.p + 1) // 4, self.p)

        # Find q and s: Q2^s

        Q = self.p - 1
        s = 0

        while Q % 2 == 0:
            s += 1
            Q //= 2

        z = 2

        while TonelliShanks.criterio_eulero(z, self.p) != (-1 % self.p):
            z += 1

        M = s
        c = pow(z, Q, self.p)
        t = pow(self.n, Q, self.p)
        R = pow(self.n, (Q + 1) // 2, self.p)

        while t != 1:
            i = 0
            temp = t

            while temp != 1:
                i += 1
                temp = pow(temp, 2, self.p)

            pow2 = pow(2, M - i - 1)
            b = pow(c, pow2, self.p)
            M = i
            c = pow(b, 2, self.p)
            t = (t * b * b) % self.p
            R = (R * b) % self.p

        return R



if __name__ == "__main__":
    n = 5
    p = 41

    ts = TonelliShanks(n, p)
    r = ts.run()
    print(r)
