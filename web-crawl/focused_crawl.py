from bs4 import BeautifulSoup
import time
import requests
import re

class Queue:
    def __init__(self):
        self.queue = []

    def push(self, element):
        self.queue.insert(0, element)

    def pop(self):
        return self.queue.pop()

    def is_empty(self):
        return len(self.queue) == 0

seed_link = 'https://en.wikipedia.org/wiki/Solar_eclipse'
max_crawl_depth = 6
bfs_frontier = Queue()
bfs_crawled_links = set([])

def focussed_web_crawl(keywords, parent_url, unique_set = set([])):
    links_explored = set([])
    wiki_prefix = 'https://en.wikipedia.org'
    #time.sleep(1)   # politeness policy for crawler
    seed = requests.get(parent_url).text
    soup = BeautifulSoup(seed, 'html.parser').find('div', {'id' : 'mw-content-text'})   # getting all content text only
    anchor = soup.find_all('a', {'href' : re.compile("^/wiki")})    # getting only wiki links
    for a in anchor:
        if is_relevant_link(keywords, str(a)):
            link = a.get('href')
            url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
            if url_filter:
                link = wiki_prefix + link
                unique_set.add(str(link))
                links_explored.add(str(link))
            if len(unique_set) >= 1000:
                break
    #print("With Root: ",parent_url," Num of Links: ",len(bfs_crawled_links))
    return list(links_explored)

def bfs_focussed(seed_url, keywords):
    global bfs_crawled_links, bfs_frontier
    current_depth = 1
    bfs_frontier.push(seed_url)
    next_depth_links = []
    while current_depth < 7:
        print("Unique Links: ",len(bfs_crawled_links))
        to_crawl = bfs_frontier.pop()
        next_depth_links += focussed_web_crawl(keywords, to_crawl, bfs_crawled_links)
        if bfs_frontier.is_empty():
            current_depth += 1
            bfs_frontier.queue = list(next_depth_links)
            next_depth_links = []
        if len(bfs_crawled_links) >= 1000:
            file_name = 'bfs_crawled_links.txt'
            #print_links(bfs_crawled_links, current_depth)
            #write_links(bfs_crawled_links, current_depth, filename)
            break

def is_relevant_link(keywords, link):
    check = link.lower()
    res = False
    for word in keywords:
        word_check = word.lower()
        res = res or (word_check in check)
    return res

def write_links(link_list, depth_reached, file_name):
    with open(file_name, 'w') as outfile:
        for link in link_list:
            outfile.write("%s\n" %link)
        outfile.write("Depth Crawled: %d" %depth_reached)

def print_links(link_list, depth_reached):
    for link in link_list:
        print(str(link))
    print("Depth Crawled: ",depth_reached)
    print("Number of Links Crawled: ",len(link_list))

bfs_focussed(seed_link, ['lunar', 'Moon'])