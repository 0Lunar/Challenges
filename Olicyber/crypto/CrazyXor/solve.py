import math
import random


target_primes_set = {2, 3, 33827, 5, 7, 11, 43, 587, 5653, 2137, 55291, 571, 254783}
enc = [209, 158, 3, 65, 15, 65, 166, 161, 78, 97, 161, 131, 202, 142, 21, 108, 94, 13, 89, 76, 239, 236, 234, 224, 240, 11, 171, 39, 139, 102, 189, 190, 163, 47, 221, 235, 131, 156, 44, 76, 228, 148, 179, 183, 134, 246, 60, 98, 79, 82, 53, 45, 79, 136]

SECURITY = 7
MIN = 100000
MAX = 500000


def prime_factors(n):
	# Returns a list that includes prime factors with their repetitions

	p = 2
	primes = []
	while p * p <= n:
		while n % p == 0:
			primes.append(p)
			n //= p
		p += 1

	if(n > 1):
		primes.append(n)

	return primes

def crazy_xor(x):
	primes = prime_factors(x)
	res = 0

	for p1 in primes:
		for p2 in primes:
			if p1 <= p2:
				res = res ^ math.lcm(p1, p2) # Least common multiple

	return res


def get_seed(x) -> tuple[list[int], set[int]]:
    _seeds = []
    primes_set = set()
    
    for _ in range(SECURITY):
        primes = prime_factors(x)
        
        for p in primes:
            primes_set.add(p)

        _seeds.append(crazy_xor(x))
    
    return (_seeds, primes_set)


def decrypt(seed) -> (bytes | None):
    random.seed(seed)
    dec = b''
    
    for i in range(len(enc)):
        dec += bytes([enc[i] ^ random.randint(0, 255)])
    
    if dec.startswith(b'ptm'):
        return dec


if __name__ == '__main__':
    for n in range(MAX):
        seed = n*n
        flag = decrypt(seed)
        
        if flag is not None:
            print(seed, flag.decode())
            break