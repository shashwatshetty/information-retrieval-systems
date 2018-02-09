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
next_depth_links = set([])
bfs_frontier = Queue()
bfs_crawled_links = set([])
call = 0

def bfs_web_crawl(parent_url):
    global next_depth_links, bfs_crawled_links, call
    call += 1
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
    #print("For Call: ",call," With Root: ",parent_url," Num of Links: ",len(bfs_crawled_links))

def bfs_round(seed_url):
    global next_depth_links, bfs_crawled_links, bfs_frontier
    current_depth = 1
    bfs_frontier.push(seed_url)
    while current_depth < 7:
        to_crawl = bfs_frontier.pop()
        bfs_web_crawl(to_crawl)
        if bfs_frontier.is_empty():
            current_depth += 1
            bfs_frontier.queue = list(next_depth_links)
            next_depth_links = set([])
        if len(bfs_crawled_links) >= 1000:
            #print_links(current_depth)
            write_links(bfs_crawled_links, current_depth)
            break


def write_links(link_list, depth_reached):
    with open('bfs_crawled_links.txt', 'w') as outfile:
        for link in link_list:
            outfile.write("%s\n" %link)
        if len(next_depth_links) != 0:
            depth_reached += 1
        outfile.write("Depth Explored: %d" %depth_reached)

def print_links(depth_reached):
    global bfs_crawled_links
    for link in bfs_crawled_links:
        print(str(link))
    if len(next_depth_links) != 0:
        depth_reached += 1
    print("Depth Explored: ",depth_reached)
    print("Number of Links Crawled: ",len(bfs_crawled_links))

bfs_round('https://en.wikipedia.org/wiki/Solar_eclipse')