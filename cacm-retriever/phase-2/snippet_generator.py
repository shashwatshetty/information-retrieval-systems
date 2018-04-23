import json
import re

queries = {}
stop_list = []
top_100 = {}
CORPUS_LOCATION = "D:/Codes/Practise Code/information-retrieval-systems/cacm-retriever/cleaned-cacm-corpus/"

'''
    Given: a json filename and a dictionary
    Effect: populates the dictionary with the data in the json file
'''
def read_from_json(file_name):
    global queries
    reader = open(file_name, 'r')
    queries = json.load(reader)
    reader.close()


def get_stop_words(file_name):
    global stop_list
    file = open(file_name, 'r+')
    stop_list = [l.strip() for l in file.readlines()]

'''
    Given: a text filename and a dictionary
    Effect: populates the dictionary with the query to document list mapping
'''
def read_top_100(filename, table):
    f = open(filename, 'r+')
    lines = [l.strip() for l in f.readlines()]
    for line in lines:
        terms = line.split(" ")
        q = terms[0]
        d = terms[2]
        if q in table:
            table[q].append(d)
        else:
            table[q] = [d]


'''
    Given: a list of terms and an integer n
    Returns: a list of all the n-grams in the given list
'''
def get_ngrams(terms, n):
    ngrams = []                                     # n-gram list
    for i in range(0, len(terms) - n + 1):
        ngrams.append(' '.join(terms[i : i + n]))   # generate n-grams using join
    return ngrams


def check_ngram_presence(query, doc, n):
    doc_loc = CORPUS_LOCATION + doc + ".txt"
    file = open(doc_loc, "r+")
    ngram = get_ngrams(query.split(), n)
    doc_content = file.read()
    doc_len = len(doc_content)
    for gram in ngram:
        if gram not in stop_list:
            if doc_content.find(gram) != -1 and bool(re.findall('\\b' + gram + '\\b', doc_content)):
                gram_index = doc_content.index(gram)
                snippet_start = max(gram_index - 50, 0)
                # if start index is in middle of the word, get start of the word
                if snippet_start > 0:
                    while snippet_start != 0:
                        prev_char = doc_content[snippet_start - 1]
                        if prev_char in [" ", "\n"]:
                            break
                        snippet_start -= 1
                snippet_end = min(gram_index + n + 50, doc_len)
                # if end index is in middle of the word, get end of the word
                if snippet_end < doc_len:
                    while snippet_end != doc_len - 1:
                        next_char = doc_content[snippet_end + 1]
                        if next_char in [" ", "\n"]:
                            snippet_end += 1
                            break
                        snippet_end += 1
                highlight_term = "<b>{}</b>".format(gram)
                snippet = doc_content[snippet_start:snippet_end].replace(gram, highlight_term)
                return snippet, True
    return "", False

def get_snippet(query, doc):
    n = 3
    while n > 0:
        snippet, has_matched = check_ngram_presence(query, doc, n)
        if has_matched:
            return snippet
        n -= 1
    return "No Snippet Found"


def write_snippet():
    file = open("snippets.html", "w+")
    file.write("<!DOCTYPE html>")
    for id, query in queries.items():
        file.write("{Query ID: " + id + "} <br />")
        for doc in top_100[id]:
            file.write("{Doc ID: " + doc + "} <br />")
            file.write("{Snippet} <br />")
            snippet = get_snippet(query, doc)
            file.write(snippet + "<br />")
            file.write(" {\Snippet} <br />")
            file.write("{\Doc ID: " + doc + "} <br />")
            file.write("<br \>")
        file.write("{\Query ID: " + id + "} <br />")
    file.close()


def main():
    get_stop_words("stop_words.txt")
    read_from_json("queries.json")
    read_top_100("bm25_t100_sample.txt", top_100)
    write_snippet()


if __name__ == '__main__':
    main()
