import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from tinydb import TinyDB, Query
import random

db = TinyDB('./data/onet.json')

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)
months = {
    'stycznia': 1,
    'lutego': 2,
    'marca': 3,
    'kwietnia': 4,
    'maja': 5,
    'czerwca': 6,
    'lipca': 7,
    'sierpnia': 8,
    'września': 9,
    'października': 10,
    'listopada': 11,
    'grudnia': 12
}

curr_date = datetime(year=2022, month=1, day=1)
while curr_date <= datetime(year=2023, month=9, day=1):

    i = 0
    while True:
        date_str = curr_date.strftime('%m/%d/%Y')
        driver.get('https://www.google.com/search?q=site:https://wiadomosci.wp.pl/polska&sca_esv=562162802&tbs=cdr:1,cd_min:%s,cd_max:%s&tbm=nws&ei=nR3zZIKIN9z-7_UPzO6j2Aw&start=%s&sa=N&ved=2ahUKEwjCyqq16ouBAxVc_7sIHUz3CMs4MhDx0wN6BAgEEAI&biw=1440&bih=783&dpr=2' % (date_str, date_str, i))
        # We need to accept the privacy policy, only for the initial page
        try:
            driver.find_elements(By.CSS_SELECTOR, 'form')[1].click()
            time.sleep(2)
        except:
            pass
        
        # Once we scrape all google pages
        articles = driver.find_elements(By.CSS_SELECTOR, 'div#search > div > div > div > div > div')
        if len(articles) == 0:
            time.sleep(random.randint(1, 30))
            break

        driver.find_element(By.CSS_SELECTOR, 'div#botstuff table')

        for article in articles:
            article_url = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            page = requests.get(article_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            content = ' '.join([ p.text().strip() for p in soup.find('article').find_all('p') ])
            print(content)

            print(article_url)

            # Add to the database
            db.insert({
                'title': article_title,
                'url': article_url,
                'release_date': article_date,
                'content': article_content
            })

        time.sleep(random.randint(1, 30))
        i += 10

    print('%s scraped!' % curr_date)
    curr_date += timedelta(days=1)