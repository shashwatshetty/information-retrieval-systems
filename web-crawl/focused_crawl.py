from bs4 import BeautifulSoup
import time
import requests
import re

'''
    The Queue implementation for the frontier of BFS.
'''
class Queue:
    # initialisation method, starts with an empty queue
    def __init__(self):
        self.queue = []

    # method to add an element into the queue
    def push(self, element):
        self.queue.insert(0, element)

    # method to pop the element from the queue in FIFO order
    def pop(self):
        return self.queue.pop()

    # method to check if queue has any elements in it
    def is_empty(self):
        return len(self.queue) == 0

# Global variables
max_crawl_depth = 6          # max depth to be crawled
bfs_frontier = Queue()       # bfs queue object
bfs_crawled_links = set([])  # unique links got by BFS crawling

'''
    Given: a list of keywords, a url and an optional set to store all the links
    Returns: list of all urls that are outlinks in the given url that match any of the words
             given in the keyword list
'''
def focused_web_crawl(keywords, parent_url, unique_set = set([])):
    links_explored = set([])                                                            # set of links contained in the given url
    wiki_prefix = 'https://en.wikipedia.org'                                            # wikipedia prefix for all sub links
    time.sleep(1)                                                                       # politeness policy for crawler
    seed = requests.get(parent_url).text
    soup = BeautifulSoup(seed, 'html.parser').find('div', {'id' : 'mw-content-text'})   # getting all content text only
    anchor = soup.find_all('a', {'href' : re.compile("^/wiki")})                        # getting only wiki links
    for a in anchor:
        if is_relevant_link(keywords, str(a)):                                          # exploration happens only if keyword present in link
            link = a.get('href')
            url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
            if url_filter:
                link = wiki_prefix + link                       # add prefix to links
                unique_set.add(str(link))                       # stored in set, so no duplicates will be there
                links_explored.add(str(link))
            if len(unique_set) >= 1000:                         # stop when 1000 unique links found
                break
    #print("With Root: ",parent_url," Num of Links: ",len(bfs_crawled_links))
    return list(links_explored)

'''
    Given: the seed url and a list of keywords
    Effect: creates a .txt file which contains 1000 unique links explored in BFS order
            starting from the given seed url containing any of the words in the keyword list.
'''
def bfs_focused(seed_url, keywords):
    global bfs_crawled_links, bfs_frontier
    current_depth = 1                                                                   # initial depth of the seed
    bfs_frontier.push(seed_url)
    next_depth_links = []                                                               # links that belong to the lower depth
    while current_depth < 7:
        #print("Unique Links: ",len(bfs_crawled_links))
        to_crawl = bfs_frontier.pop()
        next_depth_links += focused_web_crawl(keywords, to_crawl, bfs_crawled_links)
        if bfs_frontier.is_empty():                                                     # when all links in current depth are crawled
            current_depth += 1
            bfs_frontier.queue = list(next_depth_links)                                 # add the next depth links in the frontier
            next_depth_links = []                                                       # make the next depth links empty
        if len(bfs_crawled_links) >= 1000:                                              # stop when 1000 links found
            file_name = 'focused_crawled_links.txt'
            #print_links(bfs_crawled_links, current_depth)
            write_links(bfs_crawled_links, current_depth, file_name)                    # write the links to file
            break

'''
    Given: a list of keywords and a link
    Returns: True iff any of the keywords are a part of the link else returns False
'''
def is_relevant_link(keywords, link):
    check = link.lower()                        # make the link lower case
    res = False
    for word in keywords:
        word_check = word.lower()               # make the keyword lower case
        res = res or (word_check in check)      # comparison will ignore cases
    return res

'''
    Given: a set of links, the depth crawled and a file name
    Effect: writes all the links in the set in a .txt file with the given file name.
'''
def write_links(link_list, depth_reached, file_name):
    with open(file_name, 'w') as outfile:
        for link in link_list:
            outfile.write("%s\n" %link)
        outfile.write("Depth Crawled: %d" %depth_reached)

'''
    Given: a set of links and the depth crawled
    Effect: prints all the links in the set on the console.
'''
def print_links(link_list, depth_reached):
    for link in link_list:
        print(str(link))
    print("Depth Crawled: ",depth_reached)
    print("Number of Links Crawled: ",len(link_list))

# main method
def main():
    num_keywords = int(input("Enter Number of Keywords\n"))
    count = 0
    keywords = []                                                   # list of keywords
    while count < num_keywords:
        word = input("Enter A Keyword\n")
        keywords.append(word)
        count += 1
    seed_link = 'https://en.wikipedia.org/wiki/Solar_eclipse'
    bfs_focused(seed_link, keywords)

if __name__ == '__main__':
    main()