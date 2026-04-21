import random


def xor(a, b):
    return bytes([x^y for x,y in zip(a,b)])


class LFSR(object):
    def __init__(self, s):
        self.s = list(map(int, s))

    def gen_stream(self, n):
        out = []
        for i in range(n):
            out.append(self.s[0])
            self.s = self.s[1:] + [self.s[0]^self.s[3]^self.s[7]^self.s[9]]
        return out


#initial_state = random.randint(0,2**56) # 2**56 = 72057594037927936, impossible to bruteforce!
#initial_state = [int(x) for x in bin(initial_state)[2:].rjust(56, '0')]
#L = LFSR(initial_state)


def checkFlag(x: bytes):
    alph = list(range(0, 127))
    
    for n in x:
        if n not in alph:
            return False
    
    return True


if __name__ == "__main__":
    with open("data.txt", "rt") as f:
        encrypted_flag = f.read().strip()
    
    encrypted_flag = bytes.fromhex(encrypted_flag)
    
    for n in range(65536):
        initial_state = b'flag{' + n.to_bytes(2, 'big')
        initial_state = xor(initial_state, encrypted_flag[:7])
        initial_state = int.from_bytes(initial_state)
        initial_state = [int(x) for x in bin(initial_state)[2:].rjust(56, '0')]

        L = LFSR(initial_state)
    
        k = b''
    
        for i in range(len(encrypted_flag)):
        	k += bytes([int("".join(str(x) for x in L.gen_stream(8)), 2)])

        flag = xor(encrypted_flag, k)
        
        if checkFlag(flag):
            print(flag.decode())