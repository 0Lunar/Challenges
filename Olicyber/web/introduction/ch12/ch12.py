#!/usr/bin/python3
#script made by LunarStone292

import requests as r
from bs4 import BeautifulSoup as bs
from colorama import Fore

uri = "http://web-12.challs.olicyber.it/"

def main():
    message = r.get(uri).text
    soup = bs(message, 'html.parser')
    text = soup.find("pre")
    text = "".join(str(text))
    text = text.split(">")[1].split("<")[0]
    return text

if __name__ == "__main__":
    text = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + text + Fore.RESET)
