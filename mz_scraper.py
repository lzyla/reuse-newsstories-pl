!pip install bs4
!pip install requests


import requests
from bs4 import BeautifulSoup

"""Parser for each news articule.

  Articles:
    'title' string: Tytuł newsu
    'date' string: Data publikacji podana przez MZ
    'intro' string: Wstęp do artykułu
    'text' string: Artykuł
"""
#number of pages
pages = 1

#list of articles
articles = []

for i in range(1, pages + 1):
    url = f'https://www.gov.pl/web/zdrowie/wiadomosci?page={str(i)}&size=10'
    page = requests.get(url)
    if page.status_code != 200:
        break
    soup = BeautifulSoup(page.content, 'html.parser')
    intro = soup.find('div', {'class': 'intro'}).text.strip()
    div = soup.find('div', {'class': 'art-prev art-prev--near-menu'})
    li_tags = div.find_all('li')


    for li in li_tags:
        link = li.find('a')
        if link:
            article_url = 'https://www.gov.pl' + link.get('href')
            article_page = requests.get(article_url)
            article_soup = BeautifulSoup(article_page.content, 'html.parser')

            title = article_soup.find('h2').text.strip()
            date = article_soup.find('p', {'class': 'event-date'}).text.strip()
            text = article_soup.find('div', {'class': 'editor-content'}).text.strip()

            articles.append({
                'title': title,
                'date': date,
                'intro': intro,
                'text': text,
            })

print(articles)