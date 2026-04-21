import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup as bs

URL = "http://xororacle.challs.olicyber.it/"


def set_secret(cookies: RequestsCookieJar, value: int) -> RequestsCookieJar:
    cookies.pop('Encrypted Secret')
    cookies['Encrypted Secret'] = f'{value:08b}'
    
    return cookies


def parse_pub_key(html: str) -> int:
    soup = bs(html, 'html.parser')
    fd = soup.find('code', attrs={"class": "lang-python"})
    
    if fd:
        return int(fd.text)
    
    return -1


if __name__ == '__main__':
    r = requests.get(URL)
    cookies = r.cookies

    cookies = set_secret(cookies, 1)
    print(cookies)
    r = requests.get(URL, cookies=cookies)
    
    print(parse_pub_key(r.text))