from bs4 import BeautifulSoup
import time
import re
import requests

seed = requests.get('https://en.wikipedia.org/wiki/Solar_eclipse').text
soup = BeautifulSoup(seed, 'html.parser')
unique_links = set()

def web_crawl(seed):
    wiki_prefix = 'https://en.wikipedia.org'
    anchor = soup.find_all('a', href = True)
    count = 1
    for a in anchor:
        link = a.get('href')
        if ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link):
            link = wiki_prefix + link
            count += 1
            print(link)
    print(count)

web_crawl(seed)