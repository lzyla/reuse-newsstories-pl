import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
import datetime

"""Parser for news and annoucements.

  Articule:
    'title' string: Tytuł wiadomości/komunikatu
    'date' string: Data publikacji podana przez MZ
    'intro' string: Wstęp do artykułu
    'text' string: Artykuł
"""
#number of pages (news)
pages_n = 86

#list of news
news = []

# Databaset
db_announcements = TinyDB('./data/gov_announcements.json')
db_news = TinyDB('./data/gov_news.json')

for i in range(1, pages_n + 1):
    url = f'https://www.gov.pl/web/zdrowie/wiadomosci?page={str(i)}&size=10'
    page = requests.get(url)
    if page.status_code != 200:
        break
    soup = BeautifulSoup(page.content, 'html.parser')

    #intro = soup.find('div', {'class': 'intro'}).text.strip()
    div = soup.find('div', {'class': 'art-prev art-prev--near-menu'})
    li_tags = div.find_all('li')


    for li in li_tags:
        link = li.find('a')
        if link:
            news_url = 'https://www.gov.pl' + link.get('href')
            news_page = requests.get(news_url)
            news_soup = BeautifulSoup(news_page.content, 'html.parser')

            try:
                title = news_soup.find('h2').text.strip()
                date = news_soup.find('p', {'class': 'event-date'}).text.strip().split('.')
                date = datetime.datetime(day=int(date[0]), month=int(date[1]), year=int(date[2])).timestamp()
                text = news_soup.find('div', {'class': 'editor-content'}).text.strip()
            except AttributeError:
                print('Skipping: %s' % news_url)
                continue

            db_news.insert({
                'title': title,
                'url': news_url,
                'release_date': date,
                'content': text
            })

    print('Page %s/%s scraped' % (i, pages_n))

#number of pages (annoucements)
pages_a = 39

#list of annoucements
annoucement = []

for i in range(1, pages_a + 1):
    url = f'https://www.gov.pl/web/zdrowie/komunikaty1?page={str(i)}&size=10'
    page = requests.get(url)
    if page.status_code != 200:
        break
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find('div', {'class': 'art-prev art-prev--near-menu'})
    li_tags = div.find_all('li')


    for li in li_tags:
        link = li.find('a')
        if link:
            annoucement_url = 'https://www.gov.pl' + link.get('href')
            annoucement_page = requests.get(annoucement_url)
            annoucement_soup = BeautifulSoup(annoucement_page.content, 'html.parser')

            try:
                title = annoucement_soup.find('h2').text.strip()
                date = annoucement_soup.find('p', {'class': 'event-date'}).text.strip().split('.')
                date = datetime.datetime(day=int(date[0]), month=int(date[1]), year=int(date[2])).timestamp()
                text = annoucement_soup.find('div', {'class': 'editor-content'}).text.strip()
            except AttributeError:
                print('Skipping: %s' % annoucement_url)
                continue

            db_announcements.insert({
                'title': title,
                'url': annoucement_url,
                'release_date': date,
                'content': text
            })

    print('Page %s/%s scraped' % (i, pages_a))

            