import json

# global variables
FOLDER_NAME = 'downloaded-files/'           # location to download the textual files
filenames = []                              # stores the name of all the files created


'''
    Given: a file name and list to store the unique crawled links
    Effect: populates the given list with the links extracted from the given file name.
'''
def get_crawled_links(file_name, crawled_links):
    with open(file_name, 'r') as file:                                                            # open file
        line = file.readlines()
    crawled_links.extend([FOLDER_NAME + l.strip().split('/wiki/')[-1] + '.txt' for l in line])    # generate file names

'''
    Given: a file name
    Returns: a list of all the words in the given file
'''
def read_text(file_name):
    terms = []                              # list of all terms
    with open(file_name, 'r') as file:      # open file
        line = file.readlines()
    for l in line:
        terms += l.strip().split()          # get each term
    return terms

'''
    Given: a list of terms and an integer n
    Returns: a list of all the n-grams in the given list
'''
def get_ngrams(terms, n):
    ngrams = []                                     # n-gram list
    for i in range(0, len(terms)):
        ngrams.append(' '.join(terms[i : i + n]))   # generate n-grams using join
    return ngrams

'''
    Given: a list of file names and an integer n
    Returns: a dictionary where keys are terms and values are dictionaries
                that contain document ID to total term count mapping
'''
def tf_inverted_indexer(file_list, n):
    term_tf = {}                                        # dict with terms as keys
    for file in file_list:
        doc_id = file.split('.txt')[0].split('/')[-1]   # make doc ID
        terms = read_text(file)                         # all terms in the file
        ngrams = get_ngrams(terms, n)                   # list of n-grams in that file
        for gram in ngrams:
            if gram in term_tf:                         # if term has been added to dict
                if doc_id in term_tf[gram]:             # if document ID has been added to value dict
                    term_tf[gram][doc_id] += 1          # increase term count by 1
                else:
                    term_tf[gram][doc_id] = 1           # if new document ID is seen, create key of document ID
            else:
                term_tf[gram] = {}                      # create value dict
                term_tf[gram][doc_id] = 1               # add key of document ID and initial term count
    return term_tf

'''
    Given: a list of file names and an integer n
    Returns: a dictionary where keys are terms and values are dictionaries
                that contain document ID to list of term positions mapping
'''
def tp_inverted_indexer(file_list, n):
    term_tp = {}                                            # dict with terms as keys
    for file in file_list:
        doc_id = file.split('.txt')[0].split('/')[-1]       # make doc ID
        terms = read_text(file)                             # all terms in the file
        ngrams = get_ngrams(terms, n)                       # list of n-grams in that file
        for i in range(len(ngrams)):
            pos = i + 1                                     # position of the term in the document
            if ngrams[i] in term_tp:                        # if term has been added to dict
                if doc_id in term_tp[ngrams[i]]:            # if document ID has been added to value dict
                    term_tp[ngrams[i]][doc_id].append(pos)  # append position to position list
                else:
                    term_tp[ngrams[i]][doc_id] = [pos]      # if new document ID is seen, create key of document ID
            else:
                term_tp[ngrams[i]] = {}                     # create value dict
                term_tp[ngrams[i]][doc_id] = [pos]          # add key of document ID and initial term position
    return term_tp

'''
    Given: a dictionary and a file name
    Effect: writes the inverted index with term frequencies to a txt file
                in the format term -> (docID, tf)
'''
def write_term_frequencies(ttf, file_name):
    with open(file_name, 'w', encoding='utf-8') as outfile:
        for t in ttf:
            outfile.write("%s\t->\t" %t)
            for d in ttf[t]:
                outfile.write("(%s,\t" % d)
                outfile.write("%s)\t" % ttf[t][d])
            outfile.write("\n")

'''
    Given: a dictionary and a filename
    Effect: writes the inverted index with term positions to a txt file
                in the format term -> (docID, pos1,pos2,...)
'''
def write_term_positions(ttp, file_name):
    with open(file_name, 'w', encoding='utf-8') as outfile:
        for t in ttp:
            outfile.write("%s\t->\t" %t)
            for d in ttp[t]:
                outfile.write("(%s\t" %d)
                for pos in range(len(ttp[t][d])):
                    if pos == len(ttp[t][d]) - 1:
                        outfile.write("%s" %ttp[t][d][pos])
                    else:
                        outfile.write("%s," %ttp[t][d][pos])
                outfile.write(")\t")
            outfile.write("\n")


'''
    Given: a dictionary and a filename
    Effect: writes the inverted index into a json file
'''
def write_to_json(inv_index, filename):
    writer = open(filename, 'w')
    json.dump(inv_index, writer)
    writer.close()

# main method
def main():
    get_crawled_links("bfs_crawled_links.txt", filenames)

    # create inverted indexes
    unigram_term_doc_tf = tf_inverted_indexer(filenames, 1)
    bigram_term_doc_tf = tf_inverted_indexer(filenames, 2)
    trigram_term_doc_tf = tf_inverted_indexer(filenames, 3)
    unigram_term_doc_tp = tp_inverted_indexer(filenames, 1)

    # write to text files
    write_term_frequencies(unigram_term_doc_tf, "unigram_tf_inverted_index.txt")
    write_term_frequencies(bigram_term_doc_tf, "bigram_tf_inverted_index.txt")
    write_term_frequencies(trigram_term_doc_tf, "trigram_tf_inverted_index.txt")
    write_term_positions(unigram_term_doc_tp, "unigram_tp_inverted_index.txt")

    # write to json files
    write_to_json(unigram_term_doc_tf, "unigram_tf_inverted_index.json")
    write_to_json(bigram_term_doc_tf, "bigram_tf_inverted_index.json")
    write_to_json(trigram_term_doc_tf, "trigram_tf_inverted_index.json")
    write_to_json(unigram_term_doc_tp, "unigram_tp_inverted_index.json")


if __name__ == '__main__':
    main()
