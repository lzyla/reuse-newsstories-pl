from bs4 import BeautifulSoup
import requests
import re
import json
from tinydb import TinyDB, Query

db = TinyDB('./data/tvpinfo.json')

MAIN_URL = 'http://www.tvp.info'
PAGES_TO_SCRAPE = 3000

def main():
    for i in range(PAGES_TO_SCRAPE):
        page = requests.get(MAIN_URL + '/polska?page=%s' % (i+1))
        soup = BeautifulSoup(page.content, 'html.parser')
        article_containers = soup.find_all('div', class_='main-mesh-box__text-container')
        js_code = soup.findAll('script')[11].string.strip().replace('\n', '').split('window.__directoryData = ')[1].replace(';','')
        articles = json.loads(js_code)['items']

        for article in articles:
            article_title = article['title']
            article_release_date = article['release_date']
            article_url = MAIN_URL + article['url']

            article_page = requests.get(article_url)
            soup = BeautifulSoup(article_page.content, 'html.parser')
            content = soup.find('div', class_='article-layout')
            paragraphs = content.find_all('p')

            article_content = ''
            for p in paragraphs:
                article_content += ' ' + p.text.strip()
            
            # Add to the database
            db.insert({
                'title': article_title,
                'url': article_url,
                'release_date': article_release_date/1_000,
                'content': article_content
            })
        print('Page %s scraped' % (i+1))

if __name__ == '__main__':
    main()