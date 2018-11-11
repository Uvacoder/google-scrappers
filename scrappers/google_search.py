import time
import json
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
    def __init__(self):
        self.result = None
        self.soup = None
        self.search_time = None
        self.term = None

    def get_time(self):
        t = time.localtime(time.time())
        return '_'.join([str(i) for i in [t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min]])
    
    def download_page(self, link):
        r = requests.Session()
        r.headers.update(HEADERS)
        r = r.get(link)
        if(r.status_code == 200):
            self.soup = BeautifulSoup(r.text, 'html5lib')

    def web_search(self, term):
        self.term = term
        self.search_time = self.get_time()
        self.soup = None
        self.download_page('https://www.google.com/search?num=100&newwindow=1&q={term}&oq={term}'.format(term=term))
        if self.soup:
            # main_section = self.soup.find("div", id="rso")
            # subsections = main_section.find_all("div", class_="bkWMgd")
            # groups = []
            # for subsection in subsections:
            #     groups.extend(subsection.find_all("div", class_="g"))
            data = []
            groups = self.soup.find_all(class_='g')
            for item in groups:
                tmp = {}
                try:
                    tmp['Title'] = item.a.text
                    tmp['Link'] = item.a['href']
                    tmp['Description'] = item.find("span", class_="st").text
                    data.append(tmp)
                except:
                    pass
            self.result =  pd.DataFrame(data, columns=['Title', 'Link', 'Description'])
            self.result_count = len(data)
        else:
            self.result = None


    def image_search(self, term):
        self.term = term
        self.search_time = self.get_time()
        self.soup = None
        self.download_page('https://www.google.com/search?yv=3&q={}&num=100&newwindow=1&tbm=isch&ijn=1&start=100&asearch=ichunk&async=_id:rg_s,_pms:s,_fmt:pc'.format(term))
        if self.soup:
            jsn = [json.loads(i.text) for i in self.soup.find_all('div', class_="rg_meta notranslate")]
            data = [{'description':i['pt'],
            'img_link':i['ou'],
            'site_link':i['ru'],
            'type':i['ity'],
            'height':i['oh'],
            'width':i['ow'],
            'thumbnail':i['tu']} for i in jsn]
            self.result = pd.DataFrame(data, columns=['description', 'img_link',
            'type', 'height', 'width', 'site_link', 'thumbnail'])
            self.result_count = len(data)
        else:
            self.result = None


    def video_search(self, term):
        self.term = term
        self.search_time = self.get_time()
        self.soup = None
        self.download_page('https://www.google.com/search?q={}&num=100&newwindow=1&source=lnms&tbm=vid&sa=X&biw=1920&bih=976'.format(term))
        if self.soup:
            data = []
            groups = self.soup.find_all(class_='g')
            for item in groups:
                tmp = {}
                tmp['Title'] = item.h3.text
                tmp['Description'] = item.find(class_='st').text
                tmp['Link'] = item.a['href']
                if(item.find(class_='vdur')):
                    tmp['Duration'] = item.find(class_='vdur').text.replace('▶','')
                else:
                    tmp['Duration'] = ''
                data.append(tmp)               
            self.result =  pd.DataFrame(data, columns=['Title', 'Link', 'Duration', 'Description'])
            self.result_count = len(data)
        else:
            self.result = None
    def save(self):
        file_name = 'data/{} @{}.csv'.format(self.term, self.search_time)
        self.result.to_csv(file_name, index=False)
        print('Saved search results as "{}"'.format(file_name))