#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

uri = "http://web-10.challs.olicyber.it/"

def main():
    message = r.put(uri).headers['X-Flag']
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
