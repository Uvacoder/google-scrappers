import json
from utils import soup_downloader
def get_image_links(search_term):
  soup = soup_downloader.get_soupped(f'https://www.google.com/search?q={search_term}&num=100&newwindow=1&source=lnms&tbm=isch&sa=X')
  image_links = [json.loads(item.text)['ou'] for item in soup.find_all('div', class_="rg_meta notranslate")]
  print(f'{len(image_links)} images found')
  return image_links


if __name__ == '__main__':
  print('\n'.join(get_image_links('cats'))) 