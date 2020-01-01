from bs4 import BeautifulSoup
import time
import requests
import collections as col
import re

# Constants
MAX_CRAWL_DEPTH = 6  # max depth to be crawled
WIKI_PREFIX = 'https://en.wikipedia.org'  # wikipedia prefix for all sub links
BFS_FILE = 'bfs_crawled_links.txt'
DFS_FILE = 'dfs_crawled_links.txt'

dfs_crawled_links = set([])  # unique links got by DFS crawling


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


'''
    Given: the seed url and depth crawled so far.
    Effect: creates a .txt file which contains 1000 unique links explored in DFS order
            starting from the given seed url.
'''


def dfs_round(crawl_link, depth_crawled):
    global dfs_crawled_links, dfs_frontier
    if depth_crawled > MAX_CRAWL_DEPTH:  # avoid nodes deeper than 6
        return
    dfs_crawled_links.add(crawl_link)
    if len(dfs_crawled_links) >= 1000:  # stop when 1000 links found
        # print_links(dfs_crawled_links, depth_crawled)
        write_links(dfs_crawled_links, MAX_CRAWL_DEPTH, DFS_FILE)  # write the links to file
        return
    next_depth_links = web_crawl(crawl_link)  # links that belong to the lower depth
    # print("Depth: ",depth_crawled)
    # print("Unique Links: ",len(dfs_crawled_links))
    if depth_crawled == MAX_CRAWL_DEPTH:  # when we have reached depth 6
        add_all_links(next_depth_links, dfs_crawled_links)  # add all links below it as explored
        return
    for link in next_depth_links:
        if len(dfs_crawled_links) < 1000:
            dfs_round(link, depth_crawled + 1)  # recursively call with depth increased by one
    return


'''
    Given: a list of links and a unique set
    Effect: adds all the links in the list to the set.
'''


def add_all_links(next_depth_links, unique_set):
    for link in next_depth_links:
        if len(unique_set) < 1000:  # stop when 1000 links are in the set
            unique_set.add(link)


def write_links(link_list, depth_reached, file_name):
    """
    Creates a .txt file containing 1000 Wikipedia links that have been crawled using either BFS or DFS strategy.
    Args:
        link_list:      set of Wikipedia links that have been crawled.
        depth_reached:  depth of the N-ary tree reached to complete crawling 1000 Wikipedia links.
        file_name:      name of the .txt file that needs to be created.
    """
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
    # dfs_round(seed_link, 1)


if __name__ == '__main__':
    main()
