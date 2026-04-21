#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

token = "http://web-06.challs.olicyber.it/token"
flag = "http://web-06.challs.olicyber.it/flag"

def main():
    s = r.Session()
    s.get(token)
    message = s.get(flag).text
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
