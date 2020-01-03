from bs4 import BeautifulSoup
import time
import requests
import collections as col
import re

# Constants
MAX_CRAWL_DEPTH = 6  # max depth to be crawled
WIKI_PREFIX = 'https://en.wikipedia.org'  # wikipedia prefix for all sub links
BFS_FILE = 'bfs_crawled_links.txt'  # file name for BFS crawled links
DFS_FILE = 'dfs_crawled_links.txt'  # file name for DFS crawled links


def web_crawl(parent_url):
    """
    Crawls the given Wikipedia URL by retrieving all the out-links contained in that webpage.
    Args:
        parent_url: the Wikipedia URL that needs to be crawled.

    Returns:
        List of out-links contained by the webpage of the given Wikipedia URL.
    """
    links_explored = set([])  # set of links contained in the given url
    time.sleep(1)  # politeness policy for crawler
    seed = requests.get(parent_url).text
    soup = BeautifulSoup(seed, 'html.parser').find('div', {'id': 'mw-content-text'})  # getting all content text only
    anchor = soup.find_all('a', {'href': re.compile("^/wiki")})  # getting only wiki links
    for a in anchor:
        link = a.get('href')
        url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
        if url_filter:
            link = WIKI_PREFIX + link  # add prefix to links
            links_explored.add(str(link))
    # print("With Root: ",parent_url," Num of Links: ",len(bfs_crawled_links))
    return list(links_explored)


def bfs_round(seed_url):
    """
    Uses a Breadth First Search algorithm to crawl 1000 Wikipedia links starting from the seed URL.
    Args:
        seed_url: the Wikipedia URL where the web crawl starts.
    """
    bfs_frontier = col.deque()  # bfs queue object
    bfs_crawled_links = set([])  # unique links got by BFS crawling
    current_depth = 1
    bfs_frontier.append(seed_url)
    next_depth_links = []  # links that belong to the lower depth
    while current_depth <= MAX_CRAWL_DEPTH:
        to_crawl = bfs_frontier.popleft()
        if to_crawl not in bfs_crawled_links:
            next_depth_links += web_crawl(to_crawl)
            bfs_crawled_links.add(to_crawl)
        if not bfs_frontier:  # when all links in current depth are crawled
            current_depth += 1
            bfs_frontier = col.deque(list(next_depth_links))
            next_depth_links = []
        if len(bfs_crawled_links) >= 1000:  # stop when 1000 links found
            write_links(bfs_crawled_links, current_depth, BFS_FILE)
            break


def dfs_round(seed_url):
    """
    Uses a Depth First Search algorithm to crawl 1000 Wikipedia links starting from the seed URL.
    Args:
        seed_url: the Wikipedia URL where the web crawl starts.
    """
    dfs_frontier = col.deque()
    dfs_crawled_links = set([])  # unique links got by DFS crawling
    current_depth = 1
    dfs_frontier.append(seed_url)
    next_depth_links = []  # links that belong to the lower depth
    while current_depth <= MAX_CRAWL_DEPTH:
        to_crawl = dfs_frontier.pop()
        if to_crawl not in dfs_crawled_links:
            next_depth_links += web_crawl(to_crawl)
            dfs_crawled_links.add(to_crawl)
        if not dfs_frontier:  # when all links in current depth are crawled
            current_depth += 1
            dfs_frontier = col.deque(list(next_depth_links))
            next_depth_links = []
        if len(dfs_crawled_links) >= 1000:  # stop when 1000 links found
            write_links(dfs_crawled_links, current_depth, DFS_FILE)
            break


def write_links(link_list, depth_reached, file_name):
    """
    Creates a .txt file containing 1000 Wikipedia links that have been crawled using either BFS or DFS strategy.
    Args:
        link_list:      set of Wikipedia links that have been crawled.
        depth_reached:  depth of the N-ary tree reached to complete crawling 1000 Wikipedia links.
        file_name:      name of the .txt file that needs to be created.
    """
    print('Writing the crawled links to file ', file_name)
    link_list = sorted(link_list)
    with open(file_name, 'w') as outfile:
        for link in link_list:
            outfile.write("%s\n" % link)
        outfile.write("Depth Crawled: %d" % depth_reached)


def print_links(link_list, depth_reached):
    """
    Prints to the console 1000 Wikipedia links that have been crawled using either BFS or DFS strategy.
    Args:
        link_list:      set of Wikipedia links that have been crawled.
        depth_reached:  depth of the N-ary tree reached to complete crawling 1000 Wikipedia links.
    """
    for link in link_list:
        print(str(link))
    print("Depth Crawled: ", depth_reached)
    print("Number of Links Crawled: ", len(link_list))


# main method
def main():
    seed_link = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    bfs_round(seed_link)
    dfs_round(seed_link)


if __name__ == '__main__':
    main()
