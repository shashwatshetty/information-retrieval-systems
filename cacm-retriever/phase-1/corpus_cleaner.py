from bs4 import BeautifulSoup
import glob
import re
from string import punctuation
import json
from pathlib import Path

# global variables
HTML_CORPUS_PATH = Path("D:/Codes/Practise Code/information-retrieval-systems/cacm-retriever/cacm-src")
TXT_CORPUS_PATH = Path("D:/Codes/Practise Code/information-retrieval-systems/cacm-retriever/cleaned-cacm-corpus/")

QUERY_FILE = "queries.txt"
QUERY_JSON_FILE = "new_queries.json"
NEW_QUERY_FILE = "new_queries.txt"


def build_corpus():
    # get list of all html files in the given source directory
    corpus_path = str(HTML_CORPUS_PATH / "*.html")
    cacm_files = glob.glob(corpus_path)

    for file in cacm_files:
        opened_file = open(file, "r")
        line = opened_file.read()

        # parse html using beautiful soup
        parsed_html = BeautifulSoup(line, 'html.parser')

        # ignore all other tags except for the headings and paragraph
        content_tags = ["pre"]
        content = ''
        for tagContent in parsed_html.find_all(content_tags):
            content = tagContent.text

        # clean the content of obtained from the html file
        content = cleaning(content, True)

        # create txt file names of the cleaned content
        new_doc_name = file.split("\\")
        new_doc_name = new_doc_name[-1].split("html")
        new_doc_name = new_doc_name[0]
        path = str(TXT_CORPUS_PATH / new_doc_name)

        # write the content to txt files in a different directory
        new_doc = open(path + "txt", 'w+')
        new_doc.write(content)
        new_doc.close()

def build_queries():
    query_dictionary = {}
    content = list()

    # reading the query file
    query_file = open(QUERY_FILE, "r")
    text = query_file.read()

    # parse html using beautiful soup
    parsed_html = BeautifulSoup(text, 'lxml')

    # ignore all other tags except for the headings and paragraph
    content_tags = ["doc"];
    for tagContent in parsed_html.find_all(content_tags):
        content.append(tagContent.text.strip())

    # writing the cleaned queries in a new txt file
    txt_writer = open(NEW_QUERY_FILE, 'w')
    for word in content:
        first = word.split(" ", 1)
        # actual query
        query = first[1]
        first = first[0].encode("ascii", "ignore")
        first = first.decode("ascii", "ignore")
        # cleaning the query
        cleaned_query = cleaning(query, False)
        txt_writer.write(str(first) + ": " + str(cleaned_query) + "\n")
        query_dictionary[int(str(first))] = cleaned_query
    txt_writer.close()

    # write query data to json
    file_writer = open(QUERY_JSON_FILE, 'w')
    json.dump(query_dictionary, file_writer)
    file_writer.close()

def cleaning(content, corpus_flag):
        # convert all text to utf-8
        ascii_encoded = content.encode("utf-8", "ignore")
        utf_decoded = ascii_encoded.decode("ascii", "ignore")
        content = str(utf_decoded)

        # remove apostrophe from terms
        content = re.sub("'", '', content)

        # ignore punctuations if the punctuation flag is set to true
        # removing . and , from terms, except from in between numbers
        pos_look_ahead = "(?<=[^0-9])[.,\']"
        pos_look_behind = "[.,\'](?=[^0-9])"
        regex = pos_look_ahead + "|" + pos_look_behind
        content = re.sub(regex, '', content)

        done_list = ["'", ".", ","]

        # list containing all punctuations except for the ones checked before
        punctuations = ""
        for char in punctuation:
            if char not in done_list:
                punctuations += char

        # creating replacement string for the unwanted punctuations
        replacement = ""
        for p in punctuations:
            replacement += " "

        # cleaning unwanted punctuations
        content = content.translate(str.maketrans(punctuations, replacement))

        # trim spaces
        content = re.sub("\n"," ",content)
        content = re.sub('\s\s+', ' ', content)
        content = re.sub('\t', ' ', content)
        content = content.lower()

        # stripping numbers and spaces at the beginning and end of the content
        if corpus_flag:
            content = content.strip('0123456789 ')
        return content

def main():
    build_corpus()
    build_queries()


if __name__ == '__main__':
    main()
