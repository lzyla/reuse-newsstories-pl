from bs4 import BeautifulSoup
import requests
import re
import json
from tinydb import TinyDB, Query
import datetime

db = TinyDB('./data/polsat.json')

MAIN_URL = 'https://www.polsatnews.pl/wyszukiwarka/?text=Polska&type=event&page='
PAGES_TO_SCRAPE = 556

def main():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36'
        }

    for i in range(PAGES_TO_SCRAPE):
        page = requests.get(MAIN_URL + str(i+1), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        article_container = soup.find('div', id='searchwrap')

        for article in article_container.find_all('article'):
            url = article.find('a')['href']
            title = article.find('h2').text
            # Polsat often has urls to external websites
            if 'polsat' not in url:
                continue

            release_date = article.find('time').text
            release_date = datetime.datetime.strptime(release_date, '%d.%m.%Y, %H:%M').timestamp()

            # Get the article content
            article_page = requests.get(url, headers=headers)
            soup = BeautifulSoup(article_page.content, 'html.parser')
            try:
                content = soup.find('div', class_='news__description').text.strip()
            except AttributeError:
                print('Skipping: %s' % url)
                continue
            content = content.replace('Twoja przeglądarka nie wspiera odtwarzacza wideo...', '')
            content = content.split('WIDEO:')[0]

             # Add to the database
            db.insert({
                'title': title,
                'url': url,
                'release_date': release_date,
                'content': content
            })
        
        print('Page %s/%s scraped' % ((i+1), PAGES_TO_SCRAPE))


if __name__ == '__main__':
    main()
