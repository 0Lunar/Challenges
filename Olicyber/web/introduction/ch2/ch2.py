#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

url = "http://web-02.challs.olicyber.it/server-records"

def main():
    message = r.get(url, params={"id": "flag"}).text
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
