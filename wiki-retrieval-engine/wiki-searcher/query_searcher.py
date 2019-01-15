import json
import math
import operator

queries = []
N = 1000
b = 0.75
k1 = 1.2
k2 = 100

'''
    Given: a filename
    Returns: a dictionary of the data structure stored in the json file
'''
def read_from_json(file_name):
    reader = open(file_name, 'r')
    table_dict = json.load(reader)
    reader.close()
    return table_dict

def create_dl_table():
    table = {}
    for term in tf_inverted_index:
        for doc in tf_inverted_index[term]:
            if doc in table:
                table[doc] += tf_inverted_index[term][doc]
            else:
                table[doc] = tf_inverted_index[term][doc]
    return table

def read_queries(file_name):
    with open(file_name, 'r') as file:                                  # open file
        line = file.readlines()
    queries.extend([l.strip().split(":")[-1] for l in line])


def get_score(doc, query):
    terms = query.split()
    score = 0
    for term in terms:
        try:
            DL = dl_table[doc]
            K = k1 * ((1-b) + (b * (DL/AVDL)))
            ri = 0
            R = 0
            ni = len(df_table[term])
            if term in tf_inverted_index and doc in tf_inverted_index[term]:
                fi = tf_inverted_index[term][doc]
            else:
                fi = 0
            qfi = terms.count(term)
            exp1 = (((ri + 0.5) / float(R - ri + 0.5)) / ((float(ni) - ri + 0.5) / (float(N) - float(ni) - R + ri + 0.5)))
            exp2 = math.log(exp1)
            exp3 = (((float(k1) + 1) * float(fi)) / (float(K) + float(fi)))
            exp4 = (((float(k2) + 1) * float(qfi)) / (float(k2) + float(qfi)))
            score += (exp2 * exp3 * exp4)
        except:
            pass
    return score

'''
    Given: a dictionary for page ranks and a file name
    Effect: writes all the page rank values sorted in decreasing value to the given filename.
'''
def write_ranks(rank, file_name, id):
    sorted_100 = sorted(rank.items(), key = operator.itemgetter(1), reverse = True)[:100]
    with open(file_name, 'w') as outfile:
        pos = 1
        for k, v in sorted_100:
            line = str(id) + " " + "Q0" + " " + " " + str(k) + " " + str(pos) + " " + str(v) + " " + "BM_25" + "\n"
            outfile.write(line)
            pos += 1

def calculate_BM_score(query):
    terms = query.split()
    bm25 = {}
    docs = []
    for term in terms:
        docs += df_table[term]
    unique_docs = list(set(docs))
    for doc in unique_docs:
        score = get_score(doc, query)
        bm25[doc] = score
    return bm25


def bm25_for_queries(queries):
    queryID = 1
    for query in queries:
        ranking = calculate_BM_score(query)
        file_name = "query-" + str(queryID) + "-BM25-results.txt"
        write_ranks(ranking, file_name, queryID)
        queryID += 1


read_queries("queries.txt")
df_table = read_from_json("unigram_df_table.json")
tf_table = read_from_json("unigram_tf_table.json")
tf_inverted_index = read_from_json("unigram_tf_inverted_index.json")
dl_table = create_dl_table()
AVDL = float(sum(tf_table.values())/1000)

def main():
    bm25_for_queries(queries)


if __name__ == '__main__':
    main()
