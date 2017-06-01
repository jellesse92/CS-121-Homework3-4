# -*- coding: utf-8 -*-
from multiprocessing import Process, Value, Manager, Queue
import helperfiles
from collections import defaultdict, Counter
import os
from io import open as iopen
from bs4 import BeautifulSoup
import time

# Programmer Flags
DEVELOPING = True
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
    frequency_queue = Queue()
    index_queue = Queue()
    indexing = []

    for directory in os.listdir(main_dir):
        collection =  main_dir + "\\" + directory
        if os.path.isfile(collection):
            continue # Skip if this file isnt a folder.
        folder = Process(target=process_directory, args=(collection, directory, frequency_queue, index_queue, filecount))
        indexing.append(folder)
        folder.start()

        # Limit Number of Processes Running at a time to
        # stop cpu overload. Could Pool as an alternative.
        if len(indexing) >= INDEX_MAX:
            # Avoid Join Time-Out cause by over-full Queue()
            for i in indexing:
                if yield_queue_values(directory, i, index_queue, frequency_queue) == "DEAD":
                    indexing.remove(i)
            indexing = []
    # One Final Yield to Ensure last of the data is fully dumped.
    for i in indexing:
        yield_queue_values(directory, indexing, index_queue, frequency_queue)

    # Get TFIDF And print any errors found while processing
    debug_log("Printing TF-IDF to files.")
    indexdict, errors = helperfiles.get_tfidf(indexdict, df, filecount.value)
    print_stats(errors)
    debug_log("Done", True)
    debug_log("Elapsed Time: " + str(time.time() - start_time), True)


def process_directory(collection, directory, termfreq, indexqueue, filecount):
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
            termfreq.put(token)
            token_value = (token, directory + '/' + doc, value);
            if token in unique_tokens:
                token_value += (unique_tokens[token],)
            indexqueue.put(token_value)
    debug_log("Finished Process for Collection " + str(directory))


def yield_queue_values(dir, i, index_queue, frequency_queue):
    debug_log("Yielding Data from Index up to Directory: " + str(dir))
    while i.is_alive():
        i.join(timeout = 1)
        while True:
            try:
                item = index_queue.get(block=False)
                indexdict[item[0]].append((item[1], item[2]))
                df[frequency_queue.get(block=False)] +=1
            except Exception:
                break
    return "DEAD"


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




