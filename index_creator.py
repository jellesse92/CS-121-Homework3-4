# -*- coding: utf-8 -*-
from multiprocessing import Process, Value, Manager, Queue, Pool
import helperfiles
from collections import defaultdict, Counter
import os
from io import open as iopen
from bs4 import BeautifulSoup
import time

# Programmer Flags
DEVELOPING = False
INDEX_MAX = 5
# Automatically Load Book-Keeping
urldict = helperfiles.get_bookkeeping("WEBPAGES_CLEAN\\bookkeeping.tsv")
# Dictionary Containing Index
indexdict = defaultdict(list)  # key = term , value = (file, tf-idf) files its in
# Term Frequency Counter
df = Counter()
# File Counter
filecount = Value('i', 0)


def debug_log(logtext: 'str', to_console = False)->None:
    # If Developer Mode is set, print logs.
    if DEVELOPING or to_console:
        print(logtext)


def create_index(main_dir="WEBPAGES_CLEAN"):

    global filecount, indexdict, df
    start_time = time.time()
    # Queues for MultiProcessing Data Gathering
    m = Manager()
    frequency_queue = m.Queue()
    index_queue = Queue()
    indexing = []

    directories = [subdir[0] for subdir in os.walk(main_dir)]
    directory_processor = Pool()
    indexing = directory_processor.map(process_directory, directories[1:])
    debug_log("Combining Indexes")
    for x in range(len(indexing)):
        df.update(indexing[x][1])
        for token in indexing[x][0]:
            indexdict[token[0]].append(token[1:])
    del indexing
    del directories

    # Get TFIDF And print any errors found while processing
    debug_log("Printing TF-IDF to files.")
    indexdict, errors = helperfiles.get_tfidf(indexdict, df, filecount.value)
    print_stats(errors)
    debug_log("Done", True)
    debug_log("Elapsed Time: " + str(time.time() - start_time), True)


def process_directory(collection):
    indexes = []
    frequencies = []
    directory = collection.split("\\")[1]
    debug_log("Starting Processing for Collection " + str(directory))
    unique_tokens = defaultdict(list)
    for doc in os.listdir(collection):
        filecount.value += 1
        page = collection + "\\" + doc
        pagefile = iopen(page, 'r', encoding="utf8")
        html = BeautifulSoup(pagefile, 'html.parser')
        unique_tokens = important_words(html, unique_tokens)
        tokens = helperfiles.get_tokens(html.get_text())
        for token, value in tokens.items():
            frequencies.append(token)
            token_value = (token, directory + '/' + doc, value);
            if token in unique_tokens:
                token_value += (unique_tokens[token],)
            indexes.append(token_value)
    debug_log("Finished Process for Collection " + str(directory))
    return indexes, frequencies


def important_words(soup, unique_words):
    if soup.find('b') is not None:
        txt = soup.find('b').text
        token = helperfiles.get_tokens(txt)
        for w in token:
            unique_words[w].append("b")
    if soup.find('h1') is not None:
        txt = soup.find('h1').text
        token = helperfiles.get_tokens(txt)
        for w in token:
            unique_words[w].append("h1")
    if soup.find('h2') is not None:
        txt = soup.find('h2').text
        token = helperfiles.get_tokens(txt)
        for w in token:
            unique_words[w].append("h2")
    if soup.find('h3') is not None:
        txt = soup.find('h2').text
        token = helperfiles.get_tokens(txt)
        for w in token:
            unique_words[w].append("h3")
    return unique_words


def print_stats(errors):
    out = open("stats.txt", "w")
    out.write(u"Unique Files Found: " + str(filecount.value) + u"\n")
    out.write(u"Unique Words Found: " + str(len(indexdict)) + u"\n")
    out.write(u"Errors" + str(errors))
    out.close()

if __name__ == '__main__':
    if not os.path.isfile("temporarydatabase.tsv"):
        debug_log("Database File Does Not Exist. Creating.")
        create_index()




