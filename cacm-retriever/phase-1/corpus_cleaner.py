from bs4 import BeautifulSoup
import glob
import re
from string import maketrans
from string import punctuation
import json

SRC = "/Users/shravanreddy/Downloads/cacm/"
Query_SRC = "/Users/shravanreddy/Desktop/Phase1-Task1,2/queries.txt"
Query_DST = "/Users/shravanreddy/Desktop/Phase1-Task1,2/newqueries.json"
DST = "/Users/shravanreddy/Downloads/ir3/"
Query_DST_TXT = "/Users/shravanreddy/Desktop/Phase1-Task1,2/newqueries.txt"


def buildCorpus():

    # get list of all text files in the given source directory
    fList = glob.glob(SRC + "*.html")
    print fList
    for file in fList :
        openedFile = open(file,"r")
        line = openedFile.read()

        parsedHtml = BeautifulSoup(line,'html.parser')

        # ignore all other tags except for the headings and paragraph
        content_tags = ["pre"];
        content = ''
        for tagContent in parsedHtml.find_all(content_tags):
            content = tagContent.text
        content = cleaning(content,True)
        newDocName = file.split("/")
        newDocName = newDocName[-1].split("html")
        newDocName = newDocName[0]
        newDoc = open(DST+newDocName+"txt", 'w+')
        newDoc.write(content)
        newDoc.close()
def buildQueries():

    query_dictionary = {}
    content = list()
    query_file  = open(Query_SRC,"r")
    text = query_file.read()

    parsedHtml = BeautifulSoup(text, 'lxml')

    # ignore all other tags except for the headings and paragraph
    content_tags = ["doc"];

    for tagContent in parsedHtml.find_all(content_tags):
        content.append(tagContent.text.strip())

    txt_writer = open(Query_DST_TXT, 'w')

    for word in content:
        first = word.split(" ",1)
        query = first[1]
        first = first[0].encode("ascii","ignore")
        first = first.decode("ascii","ignore")
        cleaned_query = cleaning(query,False)
        txt_writer.write(str(first)+": "+str(cleaned_query)+"\n")
        query_dictionary[int(str(first))] = cleaned_query

    txt_writer.close()
    fwriter = open(Query_DST, 'w')

    json.dump(query_dictionary, fwriter)
    fwriter.close()




def cleaning(content,CorpusFlag):
        # convert all text to utf-8
        ascii_encoded =  content.encode("utf-8","ignore")
        utf_decoded = ascii_encoded.decode("ascii","ignore")
        content = str(utf_decoded)


        #  remove apostrophe from terms
        content = re.sub("'",'', content)


        # ignore punctutaions if the puncatiation flag is set to true

        #removing . and , from terms but ,except from in between numbers
        posLookAhead = "(?<=[^0-9])[.,\']"
        posLoookbehind = "[.,\'](?=[^0-9])"
        regex = posLookAhead + "|" + posLoookbehind
        content = re.sub(regex, '', content)

        done_list = ["'",".",","]

        # list containing all punctuations except for the ones checked before
        punctuations = ""
        for char in punctuation:
            if char not in done_list:
                punctuations += char
        replacement = ""
        for each in punctuations:
            replacement += " "

        content = content.translate(maketrans(punctuations,replacement))

        #trim spaces
        content = re.sub("\n"," ",content)

        content = re.sub('\s\s+', ' ', content)
        content = re.sub('\t', ' ', content)



        content=content.lower()
        if CorpusFlag :
            content=content.strip('0123456789 ')
        return content



buildCorpus()
buildQueries()