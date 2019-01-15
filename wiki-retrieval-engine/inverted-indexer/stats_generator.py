import json
import operator

'''
    Given: a filename
    Returns: a dictionary of the data structure stored in the json file
'''
def read_from_json(file_name):
    reader = open(file_name, 'r')
    dict = json.load(reader)
    reader.close()
    return dict

'''
    Given: an inverted index
    Returns: a dictionary of the term to term frequency mapping
'''
def create_tf_table(inv_index):
    tf_table = {}                               # term frequency table
    for term in inv_index:
        count = sum(inv_index[term].values())   # count of that particular term across all doc IDs
        tf_table[term] = count                  # map term to count
    return tf_table


'''
    Given: an inverted index
    Returns: a dictionary of the term to documents frequency mapping
'''
def create_df_table(inv_index):
    df_table = {}                               # document frequency table
    for term in inv_index:
        docs = list(inv_index[term].keys())     # stores the list of all doc IDs the term appears in
        df_table[term] = docs                   # map term to list of doc IDs
    return df_table


'''
    Given: a term frequency table, document frequency table an integer n and a file name
    Effect: writes the list of words to be considered as stop words in the given file name
'''
def generate_stop_words(tf, df, n, file_name):
    stop = []                                               # stop words list
    doc_count = 1000                                        # corpus size
    for term in tf:
        tcount = tf[term] * n                               # calculate term count for n-grams
        dcount = ((len(df[term]) * n)/doc_count) * 100      # calculate doc count for n-grams
        if tcount >= 5500 and dcount >= 65:                 # stopping condition
            stop.append(term)
    with open(file_name, 'w', encoding='utf-8') as file:    # write list to a txt file
        for word in stop:
            file.write("%s\n" %word)


'''
    Given: a term frequency table and a file name
    Effect: writes table to the given file name with columns term : term-frequency
'''
def write_tf_tables(table, file_name):
    data = sorted(table.items(), key=operator.itemgetter(1), reverse = True)    # sort w.r.t. term frequency
    with open(file_name, 'w', encoding='utf-8') as file:
        for k, v in data:
            file.write("{} : {}\n".format(k, v))


'''
    Given: a document frequency table and a file name
    Effect: writes table to the given file name with columns term : doc-IDs : document-frequency
'''
def write_df_tables(table, file_name):
    data = sorted(table.items(), key=operator.itemgetter(0), reverse = False)   # sort w.r.t term lexicographically
    with open(file_name, 'w', encoding='utf-8') as file:
        for k, v in data:
            file.write("{} : {} : {}\n".format(k, v, len(v)))


'''
    Given: a table and a file name
    Effect: writes table to the given file name in json format
'''
def write_to_json(table, filename):
    writer = open(filename, 'w')
    json.dump(table, writer)
    writer.close()

# main method
def main():
    # construct inverted indexes from json
    unigram_inverted_index = read_from_json("unigram_tf_inverted_index.json")
    bigram_inverted_index = read_from_json("bigram_tf_inverted_index.json")
    trigram_inverted_index = read_from_json("trigram_tf_inverted_index.json")

    # create the tf tables for each n-gram
    unigram_tf_table = create_tf_table(unigram_inverted_index)
    bigram_tf_table = create_tf_table(bigram_inverted_index)
    trigram_tf_table = create_tf_table(trigram_inverted_index)

    # create the df tables for each n-gram
    unigram_df_table = create_df_table(unigram_inverted_index)
    bigram_df_table = create_df_table(bigram_inverted_index)
    trigram_df_table = create_df_table(trigram_inverted_index)

    generate_stop_words(unigram_tf_table, unigram_df_table, 1, "unigram_stopwords.txt")
    generate_stop_words(bigram_tf_table, bigram_df_table, 2, "bigram_stopwords.txt")
    generate_stop_words(trigram_tf_table, trigram_df_table, 3, "trigram_stopwords.txt")

    # write the df tables to a txt file
    write_df_tables(unigram_df_table, "unigram_df_table.txt")
    write_df_tables(bigram_df_table, "bigram_df_table.txt")
    write_df_tables(trigram_df_table, "trigram_df_table.txt")

    # write the tf tables to a txt file
    write_tf_tables(unigram_tf_table, "unigram_tf_table.txt")
    write_tf_tables(bigram_tf_table, "bigram_tf_table.txt")
    write_tf_tables(trigram_tf_table, "trigram_tf_table.txt")

    # write the tf & df tables to json files
    write_to_json(unigram_tf_table, "unigram_tf_table.json")
    write_to_json(bigram_tf_table, "bigram_tf_table.json")
    write_to_json(trigram_tf_table, "trigram_tf_table.json")
    write_to_json(unigram_df_table, "unigram_df_table.json")
    write_to_json(bigram_df_table, "bigram_df_table.json")
    write_to_json(trigram_df_table, "trigram_df_table.json")


if __name__ == '__main__':
    main()
