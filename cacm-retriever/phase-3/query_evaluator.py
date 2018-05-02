# global variables
cacm_relevance = {}     # query ID to relevant documents mapping\

# query result path
QR_PATH = "D:/Codes/Practise Code/information-retrieval-systems/cacm-retriever/phase-3/query-results/"

# BM25 query results paths
BM25_STOPPING_FILE = QR_PATH + "bm25_stopping.txt"
BM25_STOPPING_OUTPUT_FILE = "bm25_stopping_evaluation.txt"
BM25_FILE = QR_PATH + "bm25_baseline.txt"
BM25_OUTPUT_FILE = "bm25_evaluation.txt"
BM25_PSEUDO_FILE= QR_PATH + "bm25_pseudo.txt"
BM25_PSEUDO_OUTPUT_FILE = "bm25_pseudo_evaluation.txt"

# tfidf query results path
TFIDF_STOPPING_FILE = QR_PATH + "tfidf_stopping.txt"
TFIDF_STOPPING_OUTPUT_FILE = "tfidf_stopping_evaluation.txt"
TFIDF_FILE = QR_PATH + "tfidf_baseline.txt"
TFIDF_OUTPUT_FILE = "tfidf_evaluation.txt"

# query likelihood query results path
QL_STOPPING_FILE = QR_PATH + "query_likelihood_stopping.txt"
QL_STOPPING_OUTPUT_FILE = "ql_stopping_evaluation.txt"
QL_FILE = QR_PATH + "query_likelihood_baseline.txt"
QL_OUTPUT_FILE = "ql_evaluation.txt"

# lucene query results path
LUCENE_FILE = QR_PATH + "lucene_baseline.txt"
LUCENE_OUTPUT_FILE = "lucene_evaluation.txt"

'''
    Given: a text filename and a dictionary
    Effect: populates the dictionary with the query to document list mapping
'''
def get_relevance(file_name, table):
    file = open(file_name, 'r+')
    lines = [l.strip() for l in file.readlines()]       # strip for each line
    for line in lines:
        terms = line.split(" ")
        q = terms[0]                                    # query ID
        d = terms[2]                                    # doc ID
        if q in table:                                  # if query ID exists in table
            table[q].append(d)                          # append to doc list
        else:
            table[q] = [d]                              # else create new list


'''
    Given: a text filename
    Returns: the dictionary with the query to document list mapping
'''
def get_query_results(file_name):
    table = {}
    file = open(file_name, 'r+')
    lines = [l.strip() for l in file.readlines()]       # strip each line
    for line in lines:
        terms = line.split(" ")                         # split using space
        q = terms[0]                                    # query ID
        d = terms[2]                                    # doc ID
        if q in cacm_relevance:                         # if doc is relevant
            if q in table:                              # if query ID is in table
                table[q].append(d)                      # append to doc list
            else:
                table[q] = [d]                          # else create a new doc list
    return table


'''
    Given: a table of queries and a text filename
    Effect: creates a file that has the effectiveness results of the engine
'''
def query_evaluate(queries, file_name):
    evaluation = ""                                     # data to be written
    total_avg_prec = 0.0                                # initial MAP value
    total_rec_rank = 0.0                                # initial MRR value
    for qid, docs in queries.items():                   # for every query
        avg_prec = 0.0                                  # initial avg. precision value
        rec_rank = 0.0                                  # RR for current query
        total_prec = 0.0                                # sum of precision for current query
        p5 = 0.0                                        # precision @ R = 5
        p20 = 0.0                                       # precision @ R = 20
        curr_rank = 1                                   # rank count
        retrieved_doc_count = 0                         # initial value of B
        relevant_doc_count = 0                          # relevant documents retrieved count
        relevant_docs = cacm_relevance[qid]             # list of relevant docs for the query
        total_relevant_docs = len(relevant_docs)        # value of A
        for doc in docs:
            doc = doc.split(".txt")[0]
            retrieved_doc_count += 1                    # increment B
            if doc in relevant_docs:                    # if doc is relevant
                if relevant_doc_count == 0:             # if it is the first relevant doc retrieved
                    rec_rank = 1/float(curr_rank)       # set RR
                    total_rec_rank += rec_rank          # add current RR to MRR
                relevant_doc_count += 1                 # increment relevant doc count
                # sum the precision values
                total_prec += (float(relevant_doc_count)/float(retrieved_doc_count))

            # set precision @ R = 5 when rank count is 5
            if curr_rank == 5:
                p5 = float(relevant_doc_count)/float(retrieved_doc_count)

            # set precision @ R = 20 when rank count is 20
            if curr_rank == 20:
                p20 = float(relevant_doc_count) / float(retrieved_doc_count)

            # format of displaying the results for corresponding query and doc
            evaluation += qid + "\t" + str(curr_rank) + "\t" + doc + "\t"
            evaluation += str(relevant_doc_count) + "/" + str(retrieved_doc_count) + "\t"
            evaluation += str(relevant_doc_count) + "/" + str(total_relevant_docs) + "\n"
            curr_rank += 1                              # increment rank

        # set avg. precision value
        if total_prec != 0.0:
            avg_prec = total_prec/relevant_doc_count
        total_avg_prec += avg_prec

        # format of displaying the results for avg. precision, RR, P@5 and P@20
        evaluation += "\nAvg. Precision:\t" + str(avg_prec) + "\n"
        evaluation += "Reciprocal Rank:\t" + str(rec_rank) + "\n"
        evaluation += "Precision @ 5:\t" + str(p5) + "\t"
        evaluation += "Precision @ 20:\t" + str(p20) + "\n\n"

    mean_avg_prec = total_avg_prec/len(cacm_relevance)      # set MAP value
    mean_rec_rank = total_rec_rank/len(cacm_relevance)      # set MRR value

    # format of displaying the results for MAP and MRR
    evaluation += "\nMean Average Precision:\t" + str(mean_avg_prec) + "\n"
    evaluation += "Mean Reciprocal Rank:\t" + str(mean_rec_rank) + "\n"

    # call function to write the results
    write_evaluation_results(file_name, evaluation)


'''
    Given: a text filename and a string containing results
    Effect: writes the string to the given filename
'''
def write_evaluation_results(file_name, result):
    file = open(file_name, 'w+')
    file.write(result)
    file.close()


def main():
    # get relevant documents for queries
    get_relevance("cacm.rel.txt", cacm_relevance)

    # generate effectiveness results for BM25 Baseline model
    bm25_query_results = get_query_results(BM25_FILE)
    query_evaluate(bm25_query_results, BM25_OUTPUT_FILE)

    # generate effectiveness results for BM25 Baseline model with stopping
    bm25_stopping_query_results = get_query_results(BM25_STOPPING_FILE)
    query_evaluate(bm25_stopping_query_results, BM25_STOPPING_OUTPUT_FILE)

    # generate effectiveness results for BM25 Baseline model with PRF
    bm25_psuedo_query_results = get_query_results(BM25_PSEUDO_FILE)
    query_evaluate(bm25_psuedo_query_results, BM25_PSEUDO_OUTPUT_FILE)

    # generate effectiveness results for Apache Lucene Baseline model
    lucene_query_results = get_query_results(LUCENE_FILE)
    query_evaluate(lucene_query_results, LUCENE_OUTPUT_FILE)

    # generate effectiveness results for TF-IDF Baseline model
    tfidf_query_results = get_query_results(TFIDF_FILE)
    query_evaluate(tfidf_query_results, TFIDF_OUTPUT_FILE)

    # generate effectiveness results for TF-IDF Baseline model with stopping
    tfidf_stopping_query_results = get_query_results(TFIDF_STOPPING_FILE)
    query_evaluate(tfidf_stopping_query_results, TFIDF_STOPPING_OUTPUT_FILE)

    # generate effectiveness results for Query Likelihood Baseline model
    ql_query_results = get_query_results(QL_FILE)
    query_evaluate(ql_query_results, QL_OUTPUT_FILE)

    # generate effectiveness results for Query Likelihood Baseline model with stopping
    ql_stopping_query_results = get_query_results(QL_STOPPING_FILE)
    query_evaluate(ql_stopping_query_results, QL_STOPPING_OUTPUT_FILE)


if __name__ == '__main__':
    main()
