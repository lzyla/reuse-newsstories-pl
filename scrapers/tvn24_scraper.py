import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tinydb import TinyDB, Query

db = TinyDB('./data/tvn24.json')

PAGES_TO_SCRAPE = 2000

def main():
    for i in range(PAGES_TO_SCRAPE):
        r = requests.get('https://tvn24.pl/polska/%s' % (i+1))
        soup = BeautifulSoup(r.content, 'html.parser')

        articles_container = soup.find('section', class_='main-content-holder__content-area')

        articles = articles_container.find_all('article')

        for article in articles:
            article_title = article.find('h2').text.strip()
            article_url = article.find('a')['href']
            if 'tvn24.pl/polska/' not in article_url:
                continue

            r = requests.get(article_url)
            soup = BeautifulSoup(r.content, 'html.parser')

            try:
                date = soup.find_all('time', class_='article-top-bar__date')[0]['datetime']
                date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z').timestamp()
            except IndexError:
                continue

            content = soup.find_all('div', class_='article-element--paragraph')
            content = ' '.join([p.text for p in content])

            # Add to the database
            db.insert({
                'title': article_title,
                'url': article_url,
                'release_date': date,
                'content': content
            })
            print(article_url)


        print('Page %s scraped' % (i+1))

if __name__ == '__main__':
    main()