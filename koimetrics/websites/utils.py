import requests
from bs4 import BeautifulSoup


def check_website_exists(url):
    
    try:
        r = requests.get(url)
        return r.status_code < 400
    except:
        return False

def check_website_contains_text(url, text):
    r = requests.get(url)
    return text in r.text

def website_contains_script(url, script_url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    script_srcs = [i.get('src') for i in soup.find_all('script') if i.get('src')] 
    if script_url in script_srcs:
        return True
    else:
        return False
