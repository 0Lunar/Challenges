#!/usr/bin/python3
#script made by LunarStone292

from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests as r
from colorama import Fore

url = "http://web-14.challs.olicyber.it/"

def main():
    index = r.get(url).text
    soup = bs(index, 'html.parser')
    message = soup.find_all(string=lambda string: isinstance(string, Comment))
    message = message[1].split(":")[1].split(" ")[1]
    return message

if __name__ == "__main__":
    message = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + message + Fore.RESET)