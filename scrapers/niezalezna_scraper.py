import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tinydb import TinyDB, Query

db = TinyDB('./data/niezalezna.json')

for i in range(1, 833):
    page = requests.get('https://niezalezna.pl/polska?page=%s' % (i+1))
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all('div', class_='item-news')

    for article in articles:
        a = article.find('a')
        url = a['href']
        title = a.text.strip()

        if 'vod.gazetapolska' in url:
            continue

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        date = soup.find('span', class_='article-date').text.strip()
        date = datetime.strptime(date, '%d.%m.%Y %H:%M').timestamp()

        content = soup.find('p', class_='lead').text.strip()
        content += ' ' + ' '.join([p.text.strip().replace('\n', ' ') for p in soup.find('div', class_='body').find_all('p')])

        print(url)

        # Add to the database
        db.insert({
            'title': title,
            'url': url,
            'release_date': date,
            'content': content
        })
    print('Page %s scraped!' % (i+1))