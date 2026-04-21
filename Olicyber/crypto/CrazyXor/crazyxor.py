#!/bin/python3.10
import math
import random

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

seeds = []
primes_set = set()

SECURITY = 7
MIN = 100000
MAX = 500000

for t in range(SECURITY):
	x = random.randint(MIN, MAX)
	
	primes = prime_factors(x)
	for p in primes:
		primes_set.add(p)

	seeds.append(crazy_xor(x))

seed = random.choice(seeds)
seed = seed * seed # big enough to fail brute force on seed

print(seed)
print(primes_set)
print(len(primes_set))

random.seed(seed)
flag = "ptm{fake_flag}"
enc = []
for i in range(len(flag)):
	enc.append(ord(flag[i]) ^ random.randint(0, 255))
print(enc)

with open('data_leak.txt', 'w') as file:
	print(primes_set, file=file)
	print(enc, file=file)

