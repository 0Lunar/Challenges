#!/usr/bin/python3
#script made by LunarStone292

from pwn import *
from colorama import Fore

def operazione(t):
    t = t.split(" ")
    t[1] = int(t[1])
    t[2] = int(t[2])
    if "DIVISIONE_INTERA" in t[0]:
    	return int(t[1]/t[2])
    if "SOMMA" in t[0]:
        return int(t[1]+t[2])
    if "POTENZA" in t[0]:
        return int(pow(t[1],t[2]))
    if "PRODOTTO" in t[0]:
        return int(t[1]*t[2])
    if "DIFFERENZA" in t[0]:
        return int(t[1]-t[2])

def main():
    print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + "Playing at 2048..." + Fore.RESET)
    conn = remote("2048.challs.olicyber.it", 10007)
    data = ""
    data = conn.recvline(4092)
    data = conn.recvline(4092)
    for i in range(2048):
    	data = conn.recv(4092)
    	data = data.decode()
    	out = operazione(data)
    	out = str(out)
    	out += "\n"
    	conn.send(out.encode())
    data = conn.recv(4092)
    data = data.decode()
    if "flag" in data:
        data = str(data.split(":")[1].split(" ")[1])
        return data

if __name__ == "__main__":
    data = main()
    if "flag" in data:
        print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + "Flag found!" + Fore.RESET)
        print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + "Flag: " + Fore.YELLOW + data + Fore.RESET)
    else:
        print("[" + Fore.RED + "+" + Fore.RESET + "]" + Fore.RED + " Flag not found" + Fore.RESET)