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

max_crawl_depth = 6
bfs_frontier = Queue()
bfs_crawled_links = set([])
dfs_crawled_links = set([])

def web_crawl(parent_url, unique_set = set([])):
    links_explored = set([])
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
            unique_set.add(str(link))
            links_explored.add(str(link))
        if len(unique_set) >= 1000:
            break
    #print("With Root: ",parent_url," Num of Links: ",len(bfs_crawled_links))
    return list(links_explored)

def bfs_round(seed_url):
    global bfs_crawled_links, bfs_frontier
    current_depth = 1
    bfs_frontier.push(seed_url)
    next_depth_links = []
    while current_depth <= max_crawl_depth:
        to_crawl = bfs_frontier.pop()
        next_depth_links += web_crawl(to_crawl, bfs_crawled_links)
        if bfs_frontier.is_empty():
            current_depth += 1
            bfs_frontier.queue = list(next_depth_links)
            next_depth_links = []
        if len(bfs_crawled_links) >= 1000:
            file_name = 'bfs_crawled_links.txt'
            #print_links(bfs_crawled_links, current_depth)
            write_links(bfs_crawled_links, current_depth, file_name)
            break
count = 0
def dfs_round(crawl_link, depth_crawled):
    global dfs_crawled_links, dfs_frontier,count
    if depth_crawled > max_crawl_depth:
        return
    dfs_crawled_links.add(crawl_link)
    if len(dfs_crawled_links) >= 1000:
        file_name = 'dfs_crawled_links.txt'
        #print_links(dfs_crawled_links, depth_crawled)
        write_links(dfs_crawled_links, max_crawl_depth, file_name)
        return
    next_depth_links = web_crawl(crawl_link)
    #print("Depth: ",depth_crawled)
    #print("Unique Links: ",len(dfs_crawled_links))
    if depth_crawled == max_crawl_depth:
        add_all_links(next_depth_links, dfs_crawled_links)
        return
    for link in next_depth_links:
        if len(dfs_crawled_links) < 1000:
            dfs_round(link, depth_crawled + 1)
    return

def add_all_links(next_depth_links, unique_set):
    for link in next_depth_links:
        if len(unique_set) < 1000:
            unique_set.add(link)

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

def main():
    seed_link = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    bfs_round(seed_link)
    dfs_round(seed_link, 1)

if __name__ == '__main__':
    main()