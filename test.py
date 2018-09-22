from scrappers import google_images
from scrappers import google_web_search
# print('\n'.join(google_images.get_image_links('cats')))
results = google_web_search.get_results('cats')
for item in results['data']:
    print(item['description'])