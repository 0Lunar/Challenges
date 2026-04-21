#!/usr/bin/python3
#script made by LunarStone292

from bs4 import BeautifulSoup as bs
from colorama import Fore

def main():
    soup = bs(open("./html/13.html"), 'html.parser')
    message = soup.find_all("span", {"class": "red"})
    final_message = ""
    for element in message:
        final_message += element.get_text()
    final_message = "flag{" + final_message + "}"
    return final_message

if __name__ == "__main__":
    text = main()
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + text + Fore.RESET)