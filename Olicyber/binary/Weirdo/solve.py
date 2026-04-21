class Solve(object):
    def __init__(self) -> None:
        self.the_username = bytearray(b'\xe5\xfd\x8d\x2c\xd9\x02\x6b\xc6\xe6\xce\x89\x2d\xc4\x42\x39\xd6\xf0\xce\x8b\x7b\xcc\x14\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x83\x91\xec\x4b\xa2\x71\x5a\xa2\x17\x00\x00\x00')
        self.the_password = bytearray(b'\x5d\xfe\xe6\xa1\x41\x57\x4d\x6c\x47\xc7\xb1\x9f\x86\x28\x53\x6e\x16\xcb\xdf\x6e\x51\x5d\x99\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe6\x95\x7a\x3d\x20\xf8\x1c\x3b\x17\x00\x00\x00')
                
        
    def xor(self, dst: bytearray, src: bytearray) -> None:
        for n in range(len(dst)):
            dst[n] ^= src[n]
        
    
    def memcpy(self, dst: bytearray, src: bytearray) -> None:
        for n in range(len(dst)):
            dst[n] = src[n] ^ 64
    
    
    def strlen(self, dst: bytearray) -> None:
        for n in range(len(dst)):
            dst[n] ^= 2
            
    
    def isPrintable(self, x: int) -> bool:
        return x >= 33 and x < 127
            
            
    def brute(self) -> bytes:
        out = b''
        
        for n in range(23):
            for x in range(256):
                if (self.the_username[n] ^ x ^ self.the_username[(n % 8) + 32]) & 0xFF == 0 and self.isPrintable(x):
                    out += bytes([x])
                    break
        
        for n in range(23):
            for x in range(256):
                if (self.the_password[(n % 8) + 32] + x ^ self.the_password[n]) & 0xFF == 0 and self.isPrintable(x):
                    out += bytes([x])
                    break
        
        return out
        

# La flag è lunga 23 caratteri

if __name__ == "__main__":
    solve = Solve()
    out = solve.brute()
    
    print(out.decode())