# import the required libraries
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from random import randint
from time import sleep

base_URL = 'https://metro.co.uk'
 
# get the business category
category_URL = f'{base_URL}/tag/business/'

# set the initial page count to 1
page_count = 1
 

data_list = []


def fetch_article_urls(base_url, page_limit):

    data_links  = []

    for i in range(0, page_limit):
        if i == 0:
            current_page = base_url
        else:
            # append category URL to page number to get the current page
            current_page = f'{base_url}page/{i}/'
            
        response = requests.get(current_page)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
    
            #  get link cards
            articles = soup.find_all("h2",class_="metro-newsfeed-post__title")
    
            # iterate through link cards to get article unique hrefs
            for article in articles:
                link = article.find('a').get('href')

                # merge article's unique URL with the base URL
                data_links.append(link)
        else:
            print(f'Error fetching links for page {i}: {response.status_code}')

    return data_links

def article_scraper(article_url):
 
    # create a new dictionary for each article
    data = {}  
 
    try:
        sleep(randint(1,10))
        response = requests.get(article_url)
 
        soup = BeautifulSoup(response.content, 'html.parser')

        title_element = soup.find('h1', class_='post-title clear')
        data['title'] = title_element.text.strip() if title_element else ''
        
        # extract published date, handle NoneType
        published_date_element = soup.find('span', class_='post-published')
        data['published_date'] = published_date_element.text.strip().replace('Published ', '') if published_date_element else ''
 
        # extract author, handle NoneType
        author_element = soup.find('a', class_='author url fn')
        data['author'] = author_element.text.strip() if author_element else ''
 
        # extract content, handle NoneType
        content_element = soup.find('div', class_='article-body')
        data['content'] = re.sub('\r?\n|\r?\t', ' ', content_element.text).strip() if content_element else ''
 
        # append the data for this article to the list
        data_list.append(data)

    except requests.RequestException as e:
        print(f'Error fetching article data for {article_url}: {e}')


article_urls = fetch_article_urls(category_URL, 10)
for article in article_urls:
    article_scraper(article)

df = pd.DataFrame(data_list)
csv_file = 'output2.csv'
df.to_csv(csv_file, index=False)




 
