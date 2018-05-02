import json
import re
import operator

# global variables
queries = {}            # dictionary of queries
stop_list = []          # list of stop words
top_100 = {}            # dictionary of the top 100 results
unigram_tf_table = {}   # unigram term frequency table

# location where Corpus is stored
CORPUS_LOCATION = "D:/Codes/Practise Code/information-retrieval-systems/cacm-retriever/cleaned-cacm-corpus/"


'''
    Given: a json filename
    Returns: a dictionary with the data in the json file
'''
def read_from_json(file_name):
    reader = open(file_name, 'r')
    table = json.load(reader)       # read from the json file
    reader.close()
    return table


'''
    Given: a term frequency dictionary
    Effect: populates the stop words list as the top 10 most frequent words
'''
def get_stop_words(table):
    tf_list = sorted(table.items(), key=operator.itemgetter(1), reverse=True)
    for k, v in tf_list[:11]:
        stop_list.append(k)


'''
    Given: a text filename and a dictionary
    Effect: populates the dictionary with the query to document list mapping
'''
def read_top_100(filename, table):
    file = open(filename, 'r+')
    lines = [l.strip() for l in file.readlines()]       # strip each line
    for line in lines:
        terms = line.split(" ")                         # split using space
        q = terms[0]                                    # query ID
        d = terms[2]                                    # doc ID
        if q in table:                                  # if query ID exists in table
            table[q].append(d)                          # append to the list of docs
        else:
            table[q] = [d]                              # else create a new list with doc


'''
    Given: a list of terms and an integer n
    Returns: a list of all the n-grams in the given list
'''
def get_ngrams(terms, n):
    ngrams = []                                     # n-gram list
    for i in range(0, len(terms) - n + 1):
        ngrams.append(' '.join(terms[i : i + n]))   # generate n-grams using join
    return ngrams


'''
    Given: a list of queries, document name and an integer n
    Returns: a snippet string and true if snippet is not empty, else false
'''
def check_ngram_presence(query, doc, n):
    doc_loc = CORPUS_LOCATION + doc + ".txt"        # create doc location string
    file = open(doc_loc, "r+")
    ngram = get_ngrams(query.split(), n)            # get n-grams of query terms
    doc_content = file.read()
    doc_len = len(doc_content)                      # length of document
    for gram in ngram:                              # for each gram
        if gram not in stop_list:                   # if not in stop list
            # checks the presence of the query term n-gram in the doc
            if doc_content.find(gram) != -1 and bool(re.findall('\\b' + gram + '\\b', doc_content)):
                gram_index = doc_content.index(gram)                # first occurrence of the query term n-gram
                snippet_start = max(gram_index - 50, 0)             # start index of snippet

                # if start index is in middle of the word, get start of the word
                if snippet_start > 0:
                    while snippet_start != 0:
                        prev_char = doc_content[snippet_start - 1]
                        if prev_char in [" ", "\n"]:
                            break
                        snippet_start -= 1
                snippet_end = min(gram_index + n + 50, doc_len)     # stop index of snippet

                # if end index is in middle of the word, get end of the word
                if snippet_end < doc_len:
                    while snippet_end != doc_len - 1:
                        next_char = doc_content[snippet_end + 1]
                        if next_char in [" ", "\n"]:
                            snippet_end += 1
                            break
                        snippet_end += 1

                # highlight the query terms in snippet
                highlight_term = "<b>{}</b>".format(gram)
                snippet = doc_content[snippet_start:snippet_end].replace(gram, highlight_term)
                return snippet, True
    return "", False


'''
    Given: a list of queries and a document name
    Returns: a snippet string for that document
'''
def get_snippet(query, doc):
    n = 3               # counter for the n-gram
    while n > 0:
        # start with trigram down to unigram
        snippet, has_matched = check_ngram_presence(query, doc, n)
        if has_matched:         # return if snippet exists
            return snippet
        n -= 1                  # else reduce counter
    return "No Snippet Found"   # return when no snippet exists for any n-gram


'''
    Effect: writes data to an html file that contains the snippet for every document
'''
def write_snippet():
    file = open("snippets.html", "w+")
    file.write("<!DOCTYPE html>")                           # doc header
    for id, query in queries.items():
        file.write("{Query ID: " + id + "} <br />")         # snippets for the query ID
        for doc in top_100[id]:                             # snippet generated from the docs
            file.write("{Doc ID: " + doc + "} <br />")
            file.write("{Snippet} <br />")
            snippet = get_snippet(query, doc)               # snippet generation call
            file.write(snippet + "<br />")
            file.write(" {\Snippet} <br />")
            file.write("{\Doc ID: " + doc + "} <br />")
            file.write("<br \>")
        file.write("{\Query ID: " + id + "} <br />")
    file.close()


def main():
    global queries, unigram_tf_table
    queries = read_from_json("queries.json")
    unigram_tf_table = read_from_json("unigrams_tf.json")
    get_stop_words(unigram_tf_table)
    read_top_100("lucene_baseline.txt", top_100)            # generate snippets for lucene
    write_snippet()


if __name__ == '__main__':
    main()
