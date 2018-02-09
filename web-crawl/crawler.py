from bs4 import BeautifulSoup
import time
import requests

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
next_depth_links = []
frontier = Queue()
bfs_crawled_links = set([])

def bfs_web_crawl(parent_url):
    global next_depth_links, bfs_crawled_links
    wiki_prefix = 'https://en.wikipedia.org'
    seed = requests.get(parent_url).text
    time.sleep(1)
    soup = BeautifulSoup(seed, 'html.parser')
    anchor = soup.find_all('a', href = True)
    count = 1
    for a in anchor:
        link = a.get('href')
        url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
        if url_filter:
            link = wiki_prefix + link
            bfs_crawled_links.add(str(link))
            next_depth_links.append(link)
        if len(bfs_crawled_links) >= 1000:
            break

def bfs_round(seed_url):
    global next_depth_links, bfs_crawled_links, frontier
    current_depth = 1
    frontier.push(seed_url)
    while current_depth < 7:
        to_crawl = frontier.pop()
        bfs_web_crawl(to_crawl)
        if frontier.is_empty():
            current_depth += 1
            frontier.queue = next_depth_links
            next_depth_links = []
        if len(bfs_crawled_links) >= 1000:
            print_links(current_depth)
            break


def write_bfs_links(depth_reached):
    with open('bfs_crawled_links.txt', 'w') as outfile:
        for link in bfs_crawled_links:
            outfile.write("%s\n" %link)
        outfile.write("Depth Crawled: %d" %depth_reached)

def print_links(depth_reached):
    global bfs_crawled_links
    for link in bfs_crawled_links:
        print(str(link))
    print("Depth Crawled: ",depth_reached)
    print("Number of Links Crawled: ",len(bfs_crawled_links))

bfs_round('https://en.wikipedia.org/wiki/Solar_eclipse')