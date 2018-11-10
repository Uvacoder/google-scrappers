import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Accept":"*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection":	"keep-alive",
  }


class Search:
    def __init__(self, term):
        self.term = term
        self.result = None
        self.soup = None
        self.search_time = None

    def get_time(self):
        t = time.localtime(time.time())
        return '_'.join([str(i) for i in [t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min]])
    
    def download_page(self, link):
        r = requests.Session()
        r.headers.update(HEADERS)
        r = r.get(link)
        if(r.status_code == 200):
            self.soup = BeautifulSoup(r.text, 'html.parser')

    def web_search(self):
        self.search_time = self.get_time()
        self.download_page('https://www.google.com/search?num=100&newwindow=1&q={term}&oq={term}'.format(term=self.term))
        if self.soup:
            main_section = self.soup.find("div", id="rso")
            subsections = main_section.find_all("div", class_="bkWMgd")
            groups = []
            for subsection in subsections:
                groups.extend(subsection.find_all("div", class_="g"))
            data = []
            for item in groups:
                tmp = {}
                try:
                    tmp['Title'] = item.a.text
                    tmp['Link'] = item.a['href']
                    tmp['Description'] = item.find("span", class_="st").text
                    data.append(tmp)
                except:
                    pass
            self.result =  pd.DataFrame(data)
        else:
            self.result = None


    def image_search(self):
        pass


    def video_search(self):
        pass
    
    def save(self):
        file_name = 'data/{} @{}.csv'.format(self.term, self.search_time)
        self.result.to_csv(file_name, index=False)
        print('Saved search results as "{}"'.format(file_name))