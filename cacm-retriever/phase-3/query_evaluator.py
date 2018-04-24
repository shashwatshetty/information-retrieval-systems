cacm_relevance = {}
# query result path
QR_PATH = "D:/Codes/Practise Code/information-retrieval-systems/cacm-retriever/phase-3/query-results/"

# BM25 query results paths
BM25_STOPPING_QR = QR_PATH + "bm25-stopping/"
BM25_STOPPING_FILE_SUFFIX = "_bm25_stopping.txt"
BM25_STOPPING_OUTPUT_FILE = "bm25_stopping_evaluation.txt"
BM25_QR = QR_PATH + "bm25/"
BM25_FILE_SUFFIX = "_bm25.txt"
BM25_OUTPUT_FILE = "bm25_evaluation.txt"
BM25_PSEUDO_QR = QR_PATH + "bm25-pseudo/"
BM25_PSEUDO_FILE_SUFFIX = "_bm25_pseudo.txt"
BM25_PSEUDO_OUTPUT_FILE = "bm25_pseudo_evaluation.txt"

# tfidf query results path
TFIDF_STOPPING_QR = QR_PATH + "tfidf-stopping/"
TFIDF_STOPPING_FILE_SUFFIX = "_tfidf_stopping.txt"
TFIDF_STOPPING_OUTPUT_FILE = "tfidf_stopping_evaluation.txt"
TFIDF_QR = QR_PATH + "tfidf/"
TFIDF_FILE_SUFFIX = "_tfidf.txt"
TFIDF_OUTPUT_FILE = "tfidf_evaluation.txt"

# query likelihood query results path
QL_STOPPING_QR = QR_PATH + "ql-stopping/"
QL_STOPPING_FILE_SUFFIX = "_queryLikelyhood_stopping.txt"
QL_STOPPING_OUTPUT_FILE = "ql_stopping_evaluation.txt"
QL_QR = QR_PATH + "ql/"
QL_FILE_SUFFIX = "_queryLikelyhood.txt"
QL_OUTPUT_FILE = "ql_evaluation.txt"

# lucene query results path
LUCENE_QR = QR_PATH + "lucene/"
LUCENE_FILE_SUFFIX = "_Lucene.txt"
LUCENE_OUTPUT_FILE = "lucene_evaluation.txt"

def get_relevance(file_name, table):
    file = open(file_name, 'r+')
    lines = [l.strip() for l in file.readlines()]
    for line in lines:
        terms = line.split(" ")
        q = terms[0]
        d = terms[2]
        if q in table:
            table[q].append(d)
        else:
            table[q] = [d]


def get_query_results(file_suffix, file_location):
    table = {}
    for qid in cacm_relevance.keys():
        file_name = file_location + qid + file_suffix
        file = open(file_name, 'r+')
        lines = [l.strip() for l in file.readlines()]
        for line in lines:
            terms = line.split(" ")
            q = terms[0]
            d = terms[2]
            if q in table:
                table[q].append(d)
            else:
                table[q] = [d]
    return table


def query_evaluate(queries, file_name):
    evaluation = ""
    total_avg_prec = 0.0
    total_rec_rank = 0.0
    for qid, docs in queries.items():
        avg_prec = 0.0
        rec_rank = 0.0
        total_prec = 0.0
        p5 = 0.0
        p20 = 0.0
        curr_rank = 1
        retrieved_doc_count = 0
        relevant_doc_count = 0
        relevant_docs = cacm_relevance[qid]
        total_relevant_docs = len(relevant_docs)
        for doc in docs:
            doc = doc.split(".txt")[0]
            retrieved_doc_count += 1
            if doc in relevant_docs:
                if relevant_doc_count == 0:
                    rec_rank = 1/float(curr_rank)
                    total_rec_rank += rec_rank
                relevant_doc_count += 1
                total_prec += (float(relevant_doc_count)/float(retrieved_doc_count))
            if curr_rank == 5:
                p5 = float(relevant_doc_count)/float(retrieved_doc_count)
            if curr_rank == 20:
                p20 = float(relevant_doc_count) / float(retrieved_doc_count)
            evaluation += qid + "\t" + str(curr_rank) + "\t" + doc + "\t"
            evaluation += str(relevant_doc_count) + "/" + str(retrieved_doc_count) + "\t"
            evaluation += str(relevant_doc_count) + "/" + str(total_relevant_docs) + "\n"
            curr_rank += 1
        if total_prec != 0.0:
            avg_prec = total_prec/relevant_doc_count
        total_avg_prec += avg_prec
        evaluation += "\nAvg. Precision:\t" + str(avg_prec) + "\n"
        evaluation += "Reciprocal Rank:\t" + str(rec_rank) + "\n"
        evaluation += "Precision @ 5:\t" + str(p5) + "\t"
        evaluation += "Precision @ 20:\t" + str(p20) + "\n\n"
    mean_avg_prec = total_avg_prec/len(cacm_relevance)
    mean_rec_rank = total_rec_rank/len(cacm_relevance)
    evaluation += "\nMean Average Precision:\t" + str(mean_avg_prec) + "\n"
    evaluation += "Mean Reciprocal Rank:\t" + str(mean_rec_rank) + "\n"
    write_evaluation_results(file_name, evaluation)


def write_evaluation_results(file_name, result):
    file = open(file_name, 'w+')
    file.write(result)
    file.close()


def main():
    get_relevance("cacm.rel.txt", cacm_relevance)
    bm25_query_results = get_query_results(BM25_FILE_SUFFIX, BM25_QR)
    query_evaluate(bm25_query_results, BM25_OUTPUT_FILE)

    bm25_stopping_query_results = get_query_results(BM25_STOPPING_FILE_SUFFIX, BM25_STOPPING_QR)
    query_evaluate(bm25_stopping_query_results, BM25_STOPPING_OUTPUT_FILE)

    bm25_psuedo_query_results = get_query_results(BM25_PSEUDO_FILE_SUFFIX, BM25_PSEUDO_QR)
    query_evaluate(bm25_psuedo_query_results, BM25_PSEUDO_OUTPUT_FILE)

    lucene_query_results = get_query_results(LUCENE_FILE_SUFFIX, LUCENE_QR)
    query_evaluate(lucene_query_results, LUCENE_OUTPUT_FILE)

    tfidf_query_results = get_query_results(TFIDF_FILE_SUFFIX, TFIDF_QR)
    query_evaluate(tfidf_query_results, TFIDF_OUTPUT_FILE)

    tfidf_stopping_query_results = get_query_results(TFIDF_STOPPING_FILE_SUFFIX, TFIDF_STOPPING_QR)
    query_evaluate(tfidf_stopping_query_results, TFIDF_STOPPING_OUTPUT_FILE)

    ql_query_results = get_query_results(QL_FILE_SUFFIX, QL_QR)
    query_evaluate(ql_query_results, QL_OUTPUT_FILE)

    ql_stopping_query_results = get_query_results(QL_STOPPING_FILE_SUFFIX, QL_STOPPING_QR)
    query_evaluate(ql_stopping_query_results, QL_STOPPING_OUTPUT_FILE)



if __name__ == '__main__':
    main()



