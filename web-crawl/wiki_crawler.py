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

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def is_empty(self):
        return len(self.queue) == 0

seed_link = 'https://en.wikipedia.org/wiki/Solar_eclipse'
bfs_frontier = Queue()
bfs_crawled_links = set([])
call = 0

def web_crawl(parent_url):
    global next_depth_links, bfs_crawled_links, call
    next_depth_links = set([])
    wiki_prefix = 'https://en.wikipedia.org'
    time.sleep(1)   # politeness policy for crawler
    seed = requests.get(parent_url).text
    soup = BeautifulSoup(seed, 'html.parser').find('div', {'id' : 'mw-content-text'})   # getting all content text only
    anchor = soup.find_all('a', {'href' : re.compile("^/wiki")})    # getting only wiki links
    for a in anchor:
        link = a.get('href')
        url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
        if url_filter:
            link = wiki_prefix + link
            bfs_crawled_links.add(str(link))
            next_depth_links.add(str(link))
        if len(bfs_crawled_links) >= 1000:
            break
    #print("With Root: ",parent_url," Num of Links: ",len(bfs_crawled_links))
    return list(next_depth_links)

def bfs_round(seed_url):
    global bfs_crawled_links, bfs_frontier
    current_depth = 1
    bfs_frontier.push(seed_url)
    next_depth_links = []
    while current_depth < 7:
        to_crawl = bfs_frontier.pop()
        next_depth_links += web_crawl(to_crawl)
        if bfs_frontier.is_empty():
            current_depth += 1
            bfs_frontier.queue = list(next_depth_links)
            next_depth_links = []
        if len(bfs_crawled_links) >= 1000:
            print_links(bfs_crawled_links, current_depth)
            if len(next_depth_links) != 0:
                current_depth += 1
            #write_links(bfs_crawled_links, current_depth)
            break

def dfs_round(seed_url, depth_crawled):
    return

def write_links(link_list, depth_reached):
    with open('bfs_crawled_links.txt', 'w') as outfile:
        for link in link_list:
            outfile.write("%s\n" %link)
        outfile.write("Depth Crawled: %d" %depth_reached)

def print_links(link_list, depth_reached):
    global bfs_crawled_links
    for link in link_list:
        print(str(link))
    print("Depth Crawled: ",depth_reached)
    print("Number of Links Crawled: ",len(bfs_crawled_links))

bfs_round('https://en.wikipedia.org/wiki/Solar_eclipse')