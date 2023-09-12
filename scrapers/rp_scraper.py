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

import json


db = TinyDB('./data/rp.json')

MAIN_URL = 'https://rp.pl'
PAGES_TO_SCRAPE = 2000

# Wyborcza login details
EMAIL = 'gstark0@icloud.com'
PASSWORD = '_JdaDXP@kMjBrs6'

def main():
    # Sign in to rp.pl
    driver = webdriver.Safari()
    driver.get('https://login.gremimedia.pl/auth/realms/gremimedia/protocol/openid-connect/auth?client_id=rp&redirect_uri=https%3A%2F%2Fwww.rp.pl%2Fwybory%2Fart39012851-nowy-sondaz-ibris-dla-rzeczpospolitej-pis-bez-zmian-ko-lekko-w-gore-konfederacja-trzecia%23after-successfully-login&state=9b9dbaf1-4ef1-4c26-896e-64d31f1ef7bd&response_mode=fragment&response_type=code&scope=openid&nonce=015927f1-fef6-4652-84b2-e9afc633217e')
    driver.find_element(By.CSS_SELECTOR, 'input#username').send_keys(EMAIL)
    driver.find_element(By.CSS_SELECTOR, 'input#password').send_keys(PASSWORD)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
    time.sleep(3)
    
    for i in range(PAGES_TO_SCRAPE):
        page = requests.get('https://www.rp.pl/wydarzenia/kraj?ajax=1&page=%s' % (i+1))
        content = json.loads(page.content)['html']
        soup = BeautifulSoup(content, 'html.parser')
        articles = soup.select('a.contentLink.line-clamp-4')

        for article in articles:
            article_title = article.text.strip()
            article_url = MAIN_URL + article['href']
            print(article_url)
            
            # Load the content in Selenium
            driver.get(article_url)
            
            #driver.find_element(By.CSS_SELECTOR, 'button._agree-button_1sd3y_79').click()
            
            # Get release date
            dtime = driver.find_element(By.CSS_SELECTOR, 'span#livePublishedAtContainer').text
            dtime = datetime.strptime(dtime, '%d.%m.%Y %H:%M').timestamp()

            # Get the article content
            content_elements = driver.find_elements(By.CSS_SELECTOR, 'p.article--paragraph')
            content = ' '.join([p.text for p in content_elements])

            db.insert({
                'title': article_title,
                'url': article_url,
                'release_date': dtime,
                'content': content
            })

            time.sleep(5)

        print('Page %s scraped' % (i+1))



if __name__ == '__main__':
    main()