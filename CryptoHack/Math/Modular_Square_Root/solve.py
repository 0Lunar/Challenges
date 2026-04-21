from tonelli_shanks import TonelliShanks


if __name__ == "__main__":
    with open("output.txt", "rt") as f:
        a = int(f.readline().strip().split(" = ")[-1])
        p = int(f.readline().strip().split(" = ")[-1])

    
    ts = TonelliShanks(a, p)
    r = ts.run()
    
    print(r)