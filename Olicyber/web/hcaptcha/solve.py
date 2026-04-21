from pwn import *   # type: ignore
import time


unfiglet_nums = {
    "9": bytes.fromhex("205f5f5f5f5f5f5f5f0a2f2020205f5f2020205c0a5c5f5f5f5f202020202f0a2020202f202020202f0a20202f5f5f5f5f2f0a0a").decode(),
    "8": bytes.fromhex("20205f5f5f5f5f5f0a202f20205f5f20205c0a203e2020202020203c0a2f2020202d2d2020205c0a5c5f5f5f5f5f5f20202f0a202020202020205c2f0a").decode(),
    "7": bytes.fromhex("5f5f5f5f5f5f5f5f5f0a5c5f5f5f5f5f5f20205c0a202020202f202020202f0a2020202f202020202f0a20202f5f5f5f5f2f0a0a").decode(),
    "6": bytes.fromhex("20205f5f5f5f5f5f5f5f0a202f20205f5f5f5f5f2f0a2f2020205f5f20205c0a5c20207c5f5f5c20205c0a205c5f5f5f5f5f20202f0a202020202020205c2f0a").decode(),
    "5": bytes.fromhex("202e5f5f5f5f5f5f5f5f0a207c2020205f5f5f5f2f0a207c5f5f5f5f20205c0a202f202020202020205c0a2f5f5f5f5f5f5f20202f0a202020202020205c2f0a").decode(),
    "4": bytes.fromhex("2020205f5f5f5f5f0a20202f20207c20207c0a202f2020207c20207c5f0a2f202020205e2020202f0a5c5f5f5f5f2020207c0a20202020207c5f5f7c0a").decode(),
    "3": bytes.fromhex("5f5f5f5f5f5f5f5f0a5c5f5f5f5f5f20205c0a20205f285f5f20203c0a202f202020202020205c0a2f5f5f5f5f5f5f20202f0a202020202020205c2f0a").decode(),
    "2": bytes.fromhex("5f5f5f5f5f5f5f5f0a5c5f5f5f5f5f20205c0a202f20205f5f5f5f2f0a2f202020202020205c0a5c5f5f5f5f5f5f5f205c0a20202020202020205c2f0a").decode(),
    "1": bytes.fromhex("205f5f5f5f0a2f5f2020207c0a207c2020207c0a207c2020207c0a207c5f5f5f7c0a0a").decode(),
    "0": bytes.fromhex("5f5f5f5f5f5f5f0a5c2020205f20205c0a2f20202f5f5c20205c0a5c20205c5f2f2020205c0a205c5f5f5f5f5f20202f0a202020202020205c2f0a").decode(),
    "+": bytes.fromhex("0a2020202e5f5f0a205f5f7c20207c5f5f5f0a2f5f5f202020205f5f2f0a2020207c5f5f7c0a0a").decode(),
    "*": bytes.fromhex("0a202f5c7c5c2f5c0a5f2920202020285f5f0a5c5f20202020205f2f0a202029202020205c0a20205c2f5c7c5c2f0a").decode(),
    "-": bytes.fromhex("0a0a205f5f5f5f5f5f0a2f5f5f5f5f5f2f0a0a0a").decode()
}

context.log_level = 'info'


def find_all(text: str, to_find: str) -> list[int]:
    out = []

    for i in range(len(text)):
        if text[i:i+len(to_find)] == to_find:
            out.append(i)

    return out


def find_common(lt: list[list]) -> list:
    common = set(lt[0])

    for sl in lt[1:]:
        common &= set(sl)
    
    common = list(common)
    common.sort()

    return common


def split_nums_ascii(figlet: str) -> list[str]:
    nums = []

    _figlet = figlet.split("\n")
    spaces = [find_all(_, " ") for _ in _figlet]

    num_start = find_common(spaces) # type: ignore
    num_start = [-1] + num_start    # type: ignore
    
    for n in range(len(num_start) - 2):
        tmp = ""

        for i in range(len(_figlet)):
            tmp += _figlet[i][num_start[n]+1:num_start[n+1]].rstrip() + "\n"

        nums.append(tmp)

    return nums

    

def main() -> None:
    conn = remote("hcaptcha.challs.olicyber.it", 20007)

    conn.recvlines(2)

    for _ in range(100):
        figlet = conn.recvuntil(b'Risposta: ').decode()
        figlet = '\n'.join(figlet.split("\n")[:-1])

        nums = split_nums_ascii(figlet)
        
        out = ""
        res = 0

        for n in nums:        
            for f in unfiglet_nums:            
                if n == unfiglet_nums[f]:
                    out += f
                    break
        
        res = eval(out)
        log.info(out + " = " + str(res))

        conn.sendline(str(res).encode())

    conn.interactive()


if __name__ == "__main__":
    main()
