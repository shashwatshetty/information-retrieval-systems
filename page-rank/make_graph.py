import requests
from bs4 import BeautifulSoup
import re

bfs_crawled_links = []
dfs_crawled_links = []
bfs_in_links = {}
bfs_out_links = {}
dfs_in_links = {}
dfs_out_links = {}

def get_crawled_links(file_name, crawled_links):
    with open(file_name, 'r') as file:
        line = file.readlines()
    crawled_links.extend([l.strip() for l in line])

def get_inlinks_outlinks(url, crawled_links, in_links, out_links):
    wiki_prefix = 'https://en.wikipedia.org'
    url_href = str(url).split('/wiki/')[-1]
    out_links[url_href] = []
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser').find('div', {'id': 'mw-content-text'})
    anchor = soup.find_all('a', {'href': re.compile("^/wiki")})
    for a in anchor:
        link = a.get('href')
        url_filter = ':' not in str(link) and '#' not in str(link) and 'Main_Page' not in str(link)
        href = str(link).split('/wiki/')[-1]
        if url_filter:
            link = wiki_prefix + link
            if link in crawled_links:
                out_links[url_href].append(href)
                if href in in_links:
                    if url_href not in in_links[href]:
                        in_links[href].append(url_href)
                else:
                    in_links[href] = [url_href]


def get_links(crawled_links, in_links, out_links):
    for l in crawled_links:
        get_inlinks_outlinks(l, crawled_links, in_links, out_links)

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