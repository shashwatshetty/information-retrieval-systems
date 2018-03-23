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

def read_text(file_name):
    terms = []
    with open(file_name, 'r') as file:      # open file
        line = file.readlines()
    for l in line:
        terms += l.strip().split()          # get each term
    return terms

def get_ngrams(terms, n):
    ngrams = []
    for i in range(0, len(terms)):
        ngrams.append(' '.join(terms[i : i + n]))
    return ngrams

def tf_inverted_indexer(file_list, n):
    term_tf = {}
    for file in file_list:
        doc_id = file.split('.txt')[0].split('/')[-1]
        terms = read_text(file)
        ngrams = get_ngrams(terms, n)
        for gram in ngrams:
            if gram in term_tf:
                if doc_id in term_tf[gram]:
                    term_tf[gram][doc_id] += 1
                else:
                    term_tf[gram][doc_id] = 1
            else:
                term_tf[gram] = {}
                term_tf[gram][doc_id] = 1
    return term_tf


def tp_inverted_indexer(file_list, n):
    term_tp = {}
    for file in file_list:
        doc_id = file.split('.txt')[0].split('/')[-1]
        terms = read_text(file)
        ngrams = get_ngrams(terms, n)
        for i in range(len(ngrams)):
            pos = i + 1
            if ngrams[i] in term_tp:
                if doc_id in term_tp[ngrams[i]]:
                    term_tp[ngrams[i]][doc_id].append(pos)
                else:
                    term_tp[ngrams[i]][doc_id] = [pos]
            else:
                term_tp[ngrams[i]] = {}
                term_tp[ngrams[i]][doc_id] = [pos]
    return term_tp

'''
    Given: a set of links, the depth crawled and a file name
    Effect: writes all the links in the set in a .txt file with the given file name.
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
Given: a dictionary with inverted index for term positions and a filename
Effect: writes the 
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

def write_to_json(inv_index, filename):
    writer = open(filename, 'w')
    json.dump(inv_index, writer)
    writer.close()

# main method
def main():
    get_crawled_links("bfs_crawled_links.txt", filenames)
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
