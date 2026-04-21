#!/usr/bin/python3
#script made by LunarStone292

from bs4 import BeautifulSoup as bs
import requests as r
from colorama import Fore

uri = "http://web-04.challs.olicyber.it/users"
headers = {'Accept': 'application/xml'}

def main():
    message = r.get(uri, headers=headers).text
    soup = bs(message, 'html.parser')
    text = soup.find("user")
    text = "".join(str(text))
    text = text.split("\n")[0].split("\"")[1]
    return text

if __name__ == "__main__":
    text = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + text + Fore.RESET)
