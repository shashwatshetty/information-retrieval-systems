from bs4 import BeautifulSoup
import time
import requests
import collections as col
import re

# Global variables
max_crawl_depth = 6  # max depth to be crawled
bfs_frontier = col.deque()  # bfs queue object
bfs_crawled_links = set([])  # unique links got by BFS crawling
dfs_crawled_links = set([])  # unique links got by DFS crawling


'''
    Given: a url and an optional set to store all the links
    Returns: list of all urls that are outlinks in the given url
'''


def web_crawl(parent_url):
    links_explored = set([])  # set of links contained in the given url
    wiki_prefix = 'https://en.wikipedia.org'  # wikipedia prefix for all sub links
    time.sleep(1)  # politeness policy for crawler
    seed = requests.get(parent_url).text
    soup = BeautifulSoup(seed, 'html.parser').find('div', {'id': 'mw-content-text'})  # getting all content text only
    anchor = soup.find_all('a', {'href': re.compile("^/wiki")})  # getting only wiki links
    for a in anchor:
        link = a.get('href')
        url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
        if url_filter:
            link = wiki_prefix + link  # add prefix to links
            links_explored.add(str(link))
    # print("With Root: ",parent_url," Num of Links: ",len(bfs_crawled_links))
    return list(links_explored)


'''
    Given: the seed url
    Effect: creates a .txt file which contains 1000 unique links explored in BFS order
            starting from the given seed url.
'''


def bfs_round(seed_url):
    global bfs_crawled_links, bfs_frontier
    current_depth = 1  # initial depth of the seed
    bfs_frontier.append(seed_url)
    next_depth_links = []  # links that belong to the lower depth
    while current_depth <= max_crawl_depth:
        # print('BFS Frontier', bfs_frontier)
        to_crawl = bfs_frontier.popleft()
        if to_crawl not in bfs_crawled_links:  # checks unique links to crawl
            next_depth_links += web_crawl(to_crawl)
            bfs_crawled_links.add(to_crawl)  # adds only crawled links to unique set
        if not bfs_frontier:  # when all links in current depth are crawled
            current_depth += 1
            bfs_frontier = col.deque(list(next_depth_links))  # add the next depth links in the frontier
            next_depth_links = []  # make the next depth links empty
        if len(bfs_crawled_links) >= 1000:  # stop when 1000 links found
            file_name = 'bfs_crawled_links.txt'
            # print_links(bfs_crawled_links, current_depth)
            write_links(bfs_crawled_links, current_depth, file_name)  # write the links to file
            break


'''
    Given: the seed url and depth crawled so far.
    Effect: creates a .txt file which contains 1000 unique links explored in DFS order
            starting from the given seed url.
'''


def dfs_round(crawl_link, depth_crawled):
    global dfs_crawled_links, dfs_frontier
    if depth_crawled > max_crawl_depth:  # avoid nodes deeper than 6
        return
    dfs_crawled_links.add(crawl_link)
    if len(dfs_crawled_links) >= 1000:  # stop when 1000 links found
        file_name = 'dfs_crawled_links.txt'
        # print_links(dfs_crawled_links, depth_crawled)
        write_links(dfs_crawled_links, max_crawl_depth, file_name)  # write the links to file
        return
    next_depth_links = web_crawl(crawl_link)  # links that belong to the lower depth
    # print("Depth: ",depth_crawled)
    # print("Unique Links: ",len(dfs_crawled_links))
    if depth_crawled == max_crawl_depth:  # when we have reached depth 6
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


'''
    Given: a set of links, the depth crawled and a file name
    Effect: writes all the links in the set in a .txt file with the given file name.
'''


def write_links(link_list, depth_reached, file_name):
    link_list = sorted(link_list)
    with open(file_name, 'w') as outfile:
        for link in link_list:
            outfile.write("%s\n" % link)
        outfile.write("Depth Crawled: %d" % depth_reached)


'''
    Given: a set of links and the depth crawled
    Effect: prints all the links in the set on the console.
'''


def print_links(link_list, depth_reached):
    for link in link_list:
        print(str(link))
    print("Depth Crawled: ", depth_reached)
    print("Number of Links Crawled: ", len(link_list))


# main method
def main():
    seed_link = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    bfs_round(seed_link)
    dfs_round(seed_link, 1)


if __name__ == '__main__':
    main()
