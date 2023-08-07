from bs4 import BeautifulSoup
import requests
import re
import json
from datetime import datetime

from selenium import webdriver
from tinydb import TinyDB, Query
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


db = TinyDB('./data/wyborcza.json')

MAIN_URL = 'https://wyborcza.pl/0,75398.html'
PAGES_TO_SCRAPE = 606

# Wyborcza login details
EMAIL = 'gstark0@icloud.com'

def main():
    # Sign in to Wyborcza.pl
    driver = webdriver.Chrome()
    driver.get('https://login.wyborcza.pl/')
    driver.find_element(By.CSS_SELECTOR, 'input[type=text]').send_keys(EMAIL)
    driver.find_element(By.CSS_SELECTOR, 'input[type=password]').send_keys(PASSWORD)
    time.sleep(3)
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    driver.find_elements(By.CSS_SELECTOR, 'button[type=submit]')[2].click()
    time.sleep(3)
    
    for i in range(PAGES_TO_SCRAPE):
        page = requests.get('%s?str=%s' % (MAIN_URL, i+1))
        soup = BeautifulSoup(page.content, 'html.parser')
        articles_container = soup.find('ul', class_='index--list')
        #articles = article_containers.find_all('a', class_='index--s-headline-link')
        articles = articles_container.find_all('li', class_='index--list-item')
        for article in articles:
            a = article.find('a', class_='index--s-headline-link')
            article_title = a.text.strip()
            article_url = a['href']

            # Get release date
            dtime = ' '.join([x.strip() for x in article.find('time').text.split('|')])
            dtime = datetime.strptime(dtime, '%d.%m.%Y %H:%M').timestamp()

            # Get the article content
            driver.get(article_url)
            time.sleep(1)
            content_elements = driver.find_elements(By.CSS_SELECTOR, 'p.text--paragraph')
            content = ' '.join([p.text for p in content_elements])

            db.insert({
                'title': article_title,
                'url': article_url,
                'release_date': dtime,
                'content': content
            })

if __name__ == '__main__':
    main()