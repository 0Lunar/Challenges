#!/usr/bin/python3
#script made by LunarStone292

from bs4 import BeautifulSoup as bs
import requests as r
from colorama import Fore

uri = "http://web-15.challs.olicyber.it/"

def main():
    index = r.get(uri).text
    soup = bs(index, 'html.parser')
    for link in soup.find_all('script'):
        x = r.get(uri + link.get('src')).text
        if "flag" in x:
            message = str(x).split("*")[4].split(":")[1].split(" ")[1]
            return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)