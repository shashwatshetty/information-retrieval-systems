import requests
from bs4 import BeautifulSoup
import re

# global variables
bfs_crawled_links = []
dfs_crawled_links = []
bfs_in_links = {}
bfs_out_links = {}
dfs_in_links = {}
dfs_out_links = {}

'''
    Given: a file name and list to store the unique crawled links
    Effect: populates the given list with the links extracted from the given file name.
'''
def get_crawled_links(file_name, crawled_links):
    with open(file_name, 'r') as file:                                  # open file
        line = file.readlines()
    crawled_links.extend([l.strip() for l in line])                     # strip line of line break and add to list


'''
    Given: a url, list of crawled links and 2 dictionaries to store in-links and out-links
    Effect: populates the in-link dictionary with the given url as value for it's corresponding out-links as keys
                and the out-link dictionary with url as key & corresponding out-links as values in a list.
'''
def get_inlinks_outlinks(url, crawled_links, in_links, out_links):
    wiki_prefix = 'https://en.wikipedia.org'                                            # wikipedia main link
    url_href = str(url).split('/wiki/')[-1]                                             # wikipedia document link
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser').find('div', {'id': 'mw-content-text'})    # getting all content text only
    anchor = soup.find_all('a', {'href': re.compile("^/wiki")})                         # getting only wiki links
    for a in anchor:
        link = a.get('href')
        url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
        href = str(link).split('/wiki/')[-1]               # child document link
        if url_filter:
            link = wiki_prefix + link
            if link in crawled_links:                      # only add child link if crawled
                out_links[url_href].append(href)
                if href in in_links:                       # avoid duplicate in-links
                    if url_href not in in_links[href]:
                        in_links[href].append(url_href)
                # else:
                #     in_links[href] = [url_href]


'''
    Given: list of crawled links and 2 dictionaries to store in-links and out-links
    Effect: populates the in-link and out-link dictionaries for every url in the crawled link list
'''
def get_links(crawled_links, in_links, out_links):
    for link in crawled_links:                                          # initialise in-link & out-link dictionary keys
        link = str(link).split('/wiki/')[-1]
        in_links[link] = []
        out_links[link] = []
    for l in crawled_links:                                             # get in-links & out-links for every link
        get_inlinks_outlinks(l, crawled_links, in_links, out_links)


'''
    Given: a dictionary and a file name
    Effect: writes all the key mapped to the list of links on one line
                in a .txt file with the given file name.
'''
def write_graph(graph_links, file_name):
    with open(file_name, 'w') as outfile:
        for key in graph_links:
            outfile.write("%s" %key)
            for link in graph_links[key]:
                outfile.write("\t%s" %link)
            outfile.write("\n")


# main method
def main():
    get_crawled_links('bfs_crawled_links.txt', bfs_crawled_links)
    get_links(bfs_crawled_links, bfs_in_links, bfs_out_links)
    write_graph(bfs_in_links, 'bfs_inlinks_graph.txt')
    write_graph(bfs_out_links, 'bfs_outlinks_graph.txt')

    get_crawled_links('dfs_crawled_links.txt', dfs_crawled_links)
    get_links(dfs_crawled_links, dfs_in_links, dfs_out_links)
    write_graph(dfs_in_links, 'dfs_inlinks_graph.txt')
    write_graph(dfs_out_links, 'dfs_outlinks_graph.txt')


if __name__ == '__main__':
    main()
