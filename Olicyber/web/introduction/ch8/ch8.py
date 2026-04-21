#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

uri = "http://web-08.challs.olicyber.it/login"
headers = {'Accept': 'application/x-www-form-urlencoded'}
payload = {'username': 'admin', 'password': 'admin'}

def main():
    message = r.post(uri, headers=headers, data=payload).text
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
