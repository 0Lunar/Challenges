#!/usr/bin/python3
#script made by LunarStone292

import requests as s
from bs4 import BeautifulSoup as bs
from colorama import Fore

url = "http://infinite.challs.olicyber.it/"

def calcoli(question):
    if "pulsante" in question:
        button = str(question.split(" ")[5].split("?")[0])
        return {button: ''}
    if "Quanto fa" in question:
    	question = question.split(" ")
    	num1 = int(str(question[2]))
    	num2 = int(str(question[4].split("?")[0]))
    	ris = num1+num2
    	ris = str(ris)
    	return {"sum": ris}
    if "Quante" in question:
    	question = question.split("\"")
    	lettera = str(question[1])
    	parola = str(question[3])
    	risposta = str(len(parola.split(lettera))-1)
    	return {"letter": risposta, "submit": "Submit"}

def main():
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Searching the flag..." + Fore.RESET)
    r = s.Session()
    ris = {"": ""} 
    html = ""
    while "flag" not in html:
    	html = r.post(url, data=ris).text
    	soup = bs(html, 'html.parser')
    	question = str(soup.p).split(">")[1].split("<")[0]
    	ris = calcoli(question)
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag found!!!" + Fore.RESET)
    soup = bs(html, 'html.parser')
    flag = str(soup.p).split(">")[1].split("<")[0]
    return flag

if __name__ == "__main__":
    flag = main()
    if "flag" in flag:
        print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + flag + Fore.RESET)
    else:
        print("[" + Fore.RED + "+" + Fore.RESET + "]" + Fore.RED + " Flag not found" + Fore.RESET)