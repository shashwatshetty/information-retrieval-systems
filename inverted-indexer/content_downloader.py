from bs4 import BeautifulSoup
import requests
import re


# global variables
FOLDER_NAME = 'downloaded-files/'
bfs_crawled_links = []

'''
    Given: a file name and list to store the unique crawled links
    Effect: populates the given list with the links extracted from the given file name.
'''
def get_crawled_links(file_name, crawled_links):
    with open(file_name, 'r') as file:                                  # open file
        line = file.readlines()
    crawled_links.extend([l.strip() for l in line])                     # strip line of line break and add to list

'''
    Given: a url
    Effect: creates a file with only text content of the url in UTF encoding
'''
def download_file_content(parent_url):
    seed = requests.get(parent_url).text
    soup = BeautifulSoup(seed, 'html.parser')
    file_name = FOLDER_NAME + str(parent_url.split('/wiki/')[-1]) + ".txt"
    for anchor in soup("a"):                                        # for loop to remove citations
        refs = str(anchor.get('href'))
        if refs.startswith('#cite'):
            anchor.extract()
    for tags in soup("span"):                                       # for loop to remove span tags
        tags.extract()
    for content in soup.find_all("div", {"id": "bodyContent"}):     # considering only bodyContents
        text = content.text
        text = re.sub(r"[^0-9A-Za-z,-\.]"," ", text)                # removes special characters from text
        text = re.sub(r"(?!\d)[.,-](?!\d)"," ", text, 0)            # retains punctuations in digits only
        text = re.sub(r'\s+', ' ', text)                            # removes extra spaces
        text = text.lower()                                         # converts text to lower case
        file = open(file_name, 'w', encoding='utf-8')
        file.write(text.strip())                                    # removes extra spaces
        file.close()

'''
    Given: a list of unique urls crawled
    Effect: downloads the textual content of each link in different files
'''
def downloader(crawled_list):
    for link in crawled_list:               # downloads content for each link
        download_file_content(link)


# main method
def main():
    get_crawled_links("bfs_crawled_links.txt", bfs_crawled_links)


if __name__ == '__main__':
    main()