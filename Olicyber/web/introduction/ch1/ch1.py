#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

url = "http://web-01.challs.olicyber.it/"

def main():
    message = r.get(url).text
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
