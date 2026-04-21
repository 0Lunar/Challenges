def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x^y for x,y in zip(a,b)])

def rol8(p1: int, p2: int):
    return p1 >> (-(p2 & 7) & 7) | p1 << (p2 & 7)

def unrol8(p1: int, p2: int) -> int:
    return (p1 << (-(p2 & 7) & 7)) & 0xFF | p1 >> (p2 & 7)


if __name__ == '__main__':
    target = b'\x75\x2e\x25\x2f\x1f\xb3\xfe\x31\x4b\xbb\xcb\x6e\x41\x30\x5d\x99\x85\xb3\xb3\x6e\x43\xa2\x58\x92\x9d\x1b\x93\x5a\xa7\x9a\xad\xc8\x85\x5b\xb7\x51'
    
    target = target[::-1]
    target = bytes([(c-i) & 0xFF for i,c in enumerate(target)])
    target = bytes([unrol8(c, i & 7) for i,c in enumerate(target)])
    target = xor(target, b'\x37' * len(target))
    
    print(target)
