bfs_crawled_links = []

def get_crawled_links(filename):
    with open(filename, 'r') as file:
        line = file.readlines()
    bfs_crawled_links.extend([l.strip() for l in line])


get_crawled_links('bfs_crawled_links.txt')