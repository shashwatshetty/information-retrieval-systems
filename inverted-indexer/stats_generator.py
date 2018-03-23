import json
import operator

def read_from_json(file_name):
    reader = open(file_name, 'r')
    dict = json.load(reader)
    reader.close()
    return dict

def create_tf_table(inv_index):
    tf_table = {}
    for term in inv_index:
        count = sum(inv_index[term].values())
        tf_table[term] = count
    return tf_table

def create_df_table(inv_index):
    df_table = {}
    for term in inv_index:
        docs = list(inv_index[term].keys())
        df_table[term] = docs
    return df_table

def generate_stop_words(tf, df, n, file_name):
    stop = []
    term_count = sum(list(tf.values()))
    doc_count = 1000
    for term in tf:
        tcount = tf[term] * n
        dcount = ((len(df[term]) * n)/doc_count) * 100
        # print(tcount, dcount)
        if tcount >= 5500 and dcount >= 65:
            stop.append(term)
    with open(file_name, 'w', encoding='utf-8') as file:
        for word in stop:
            file.write("%s\n" %word)


def write_tf_tables(table, file_name):
    data = sorted(table.items(), key=operator.itemgetter(1), reverse = True)
    with open(file_name, 'w', encoding='utf-8') as file:
        for k, v in data:
            file.write("{} : {}\n".format(k, v))

def write_df_tables(table, file_name):
    data = sorted(table.items(), key=operator.itemgetter(0), reverse = False)
    with open(file_name, 'w', encoding='utf-8') as file:
        for k, v in data:
            file.write("{} : {} : {}\n".format(k, v, len(v)))

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