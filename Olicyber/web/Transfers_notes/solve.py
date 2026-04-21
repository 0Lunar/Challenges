class Solve(object):
    def __init__(self, bt: str) -> None:
        self.enc = bytes.fromhex(bt)
    
    
    def xor(self, src: bytes, bt: int):
        bt = bt & 0xFF
        nbt = bt.to_bytes(1, 'big') * len(src)
        
        return bytes([x^y for x,y in zip(src, nbt)])
    
    
    def isPrintable(self, a: bytes) -> bool:
        for x in a:
            if x < 32 or x > 125:
                return False
        
        if not any([x == 32 for x in a]):
            return False
        
        return True
    
    
    def brute(self) -> list[str]:
        out = []
        
        for x in range(256):
            if self.isPrintable(n := self.xor(self.enc, x)):
                out.append(n.decode())
                      
        return out



if __name__ == "__main__":
    solve = Solve("5964637a7a6f7e3f324e5e7050424659657d61627f61615d785d4148687c5a7b4c4945396d7f79693a6f5370693f5d3e7b617f404c6b6d615f6b43503e7079382a36272a393b3d3f383c3f4943655f4849485f392a762a7a7e6771676b6473557e3b67393f55683e6e7733487b445c63724848594d534c433b406f4962655a69")
    out = solve.brute()
    
    flag = out[0].split(" | ")[-1]
    flag = flag.split("}")[0] + "}"

    print(flag)
