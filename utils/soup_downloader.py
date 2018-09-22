import requests
from bs4 import BeautifulSoup
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Accept":"*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection":	"keep-alive",
  }

def get_soupped(url):
  r = requests.Session()
  r.headers.update(HEADERS)
  r = r.get(url)
  if(r.status_code == 200):
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
  else:
    return False