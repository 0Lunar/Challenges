def load_flag(file: str = "output.txt") -> bytes:
    with open(file, "rt") as f:
        data = f.read().strip()
    
    return bytes.fromhex(data)


def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x^y for x,y in zip(a,b)])


if __name__ == '__main__':
    const_k = 0x4B
    const_k_m_1 = 0x4A
    mod = 0x10001
    flag = b''
    enc_flag = 0x1AACF60
    enc = load_flag()
    
    for bt in enc:
        tmp = (const_k * enc_flag + const_k_m_1) % mod

        for n in range(33,127):
            if (tmp % 0x100) ^ n == bt:
                flag += bytes([n])
                enc_flag = tmp

    print(flag.decode())