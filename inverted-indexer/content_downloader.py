from bs4 import BeautifulSoup
import time
import requests
import re


# global variables
bfs_crawled_links = []

'''
    Given: a file name and list to store the unique crawled links
    Effect: populates the given list with the links extracted from the given file name.
'''
def get_crawled_links(file_name, crawled_links):
    with open(file_name, 'r') as file:                                  # open file
        line = file.readlines()
    crawled_links.extend([l.strip() for l in line])                     # strip line of line break and add to list

'''
    Given: a url and an optional set to store all the links
    Returns: list of all urls that are outlinks in the given url
'''
def web_crawl(parent_url):
    seed = requests.get(parent_url).text
    soup = BeautifulSoup(seed, 'html.parser')
    # print(soup)
    file_name = str(parent_url.split('/wiki/')[-1]) + ".txt"
    for anchor in soup("a"):                                        # for loop to remove citations
        refs = str(anchor.get('href'))
        if refs.startswith('#cite'):
            anchor.extract()
    for tags in soup("span"):                                       # for loop to remove span tags
        tags.extract()
    for content in soup.find_all("div", {"id": "bodyContent"}):     # considering only bodyContents
        text = content.text
        # print(text)
        break

    # soup = BeautifulSoup(seed, 'html.parser').find('div', {'id': 'mw-content-text'})   # getting all content text only
    # anchor = soup.find_all('a', {'href': re.compile("^/wiki")})                        # getting only wiki links
    # for a in anchor:
    #     link = a.get('href')
    #     url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
    #     if url_filter:
    #         link = wiki_prefix + link                      # add prefix to links
    #         links_explored.add(str(link))
    # # print("With Root: ",parent_url," Num of Links: ",len(bfs_crawled_links))
    # return list(links_explored)

get_crawled_links("bfs_crawled_links.txt", bfs_crawled_links)
web_crawl(bfs_crawled_links[0])