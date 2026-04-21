with open("out.txt", "rt") as f:
    data = f.read().strip().split("\n")


with open("decoded.txt", "wb") as f:
    for line in data:
        if len(line) > 0:
            dt = bytes.fromhex(line)
            f.write(dt + b'\n')
