import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tinydb import TinyDB, Query
import json

db = TinyDB('./data/natemat.json')

PAGES_TO_SCRAPE = 1813

for i in range(1, PAGES_TO_SCRAPE):
    data = requests.get('https://natemat.pl/api/posts?page=%s&categoryId=1' % (i)).text
    data = json.loads(data)
    articles = data['posts']

    for article in articles:
        title = article['title']
        url = article['url']

        if 'prognoza-pogody' in url or 'pogoda' in url:
            continue
        
        try:
            date = ':'.join(article['iso_date'].split(':')[0:-2])
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M').timestamp()

            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            header = soup.find('div', class_='lead-amp').text
            content = soup.find('section', class_='art__content').text.strip()
            content = ' '.join(content.replace('\n', ' ').split())

            # Add to the database
            db.insert({
                'title': title,
                'url': url,
                'release_date': date,
                'content': content
            })
        except:
            print('Skipped...')
            continue

    print('Page %s scraped!' % (i))

