import json
from utils import soup_downloader
TABLE_HEADERS = ['title','link','description']
def get_results(search_term):
	soup = soup_downloader.get_soupped(f'https://www.google.com/search?num=100&newwindow=1&q=cats&oq=cats')
	main_section = soup.find("div", id="rso")
	subsections = main_section.find_all("div", class_="bkWMgd")
	groups = []
	for subsection in subsections:
		groups.extend(subsection.find_all("div", class_="g"))
	data = []
	for item in groups:
		tmp = {}
		try:
			tmp['title'] = item.a.text
			tmp['link'] = item.a['href']
			tmp['description'] = item.find("span", class_="st").text
			data.append(tmp)
		except:
			pass
	return {'headers':TABLE_HEADERS, 'data':data}