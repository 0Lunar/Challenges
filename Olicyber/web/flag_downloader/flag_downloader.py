#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

def main():
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Getting the flag..." + Fore.RESET)
    n = '0'
    url = "http://flagdownloader.challs.olicyber.it/download/flag/"
    flag = ""
    while n:
        l = r.get(url+n)
        j = l.json()
        n = j['n']
        flag += j['c']
    return flag

if __name__ == "__main__":
    flag = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + flag + Fore.RESET)
