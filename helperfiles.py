# -*- coding: utf-8 -*-
from collections import defaultdict
import csv
import re
import math
import dbconnector
import ast
import io
from multiprocessing import Pool

#DATABASE MODE VS Print to File
DB_MODE = True
db_name = "database.txt"

#GLOBALS
file_index = defaultdict(list)


def get_tfidf(indexdict, n):
    tfidf = defaultdict(list)
    errors = []
    for term, value in indexdict.items():
        for pair in value:
            tf_idf = calculate_tfidf(pair[1], n / len(indexdict[term]))
            ranking = rank_important_words(tf_idf, pair[2])
            tfidf[term].append((pair[0], float(round(ranking, 2, ))))

    return tfidf, errors


def calculate_tfidf(tf, idf):
    retval = 0
    try:
        retval = (1 + math.log10(tf)) * math.log10(idf)
    except Exception as e:
        print("Error Found")
        retval = 0
    finally:
        return retval


def rank_important_words(calculation, imp_list):
    """This function is called in TfidfDict()
        tfidf values are given additional ranking if they contain tags
        t = 1.5 (b, h1, h2, h3) = 1.7

        if a word contains title, h1, and h2 then tfidf * (1.5, 1.7, 1.7)
        """
    additional_ranking = 0
    if 't' in imp_list:
        additional_ranking += 1.5
    if 'b' in imp_list:
        additional_ranking += 1.7
    if 'h1' in imp_list:
        additional_ranking += 1.7
    if 'h2' in imp_list:
        additional_ranking += 1.7
    if additional_ranking > 0:
        calculation *= additional_ranking
    return calculation


def get_bookkeeping(filename):
    urldict = dict()
    with open(filename, "r") as books:
        books = csv.reader(books, delimiter='\t')
        for row in books:
            urldict[row[0]] = row[1]
    return urldict


def write_row_db(index_values):
    #   Temporary  write to Database
    outfile = io.open(db_name, "a+", encoding='utf8')
    writer = csv.writer(outfile, delimiter='|',)
    writer.writerow(index_values)
    outfile.close()
    return


def print_to_database(tfidf):
    p = Pool()
    p.map(write_row_db, [(key.encode('utf-8'), val) for key, val in tfidf.items()])
    if DB_MODE:
        dbconnector.insert_all_data(db_name)



def get_tokens(text):
    tokens = defaultdict(int)
    text = re.sub(r'[^\w\s]',' ',text)
    for word in text.lower().strip().split():
        tokens[word] += 1
    return tokens


def query_terms(*terms) -> str:
    global file_index
    search_results = defaultdict(list)
    if DB_MODE:
        dbconnector.build_connection()
        for term in terms:
            search_results[term] = ast.literal_eval(dbconnector.query_data(term))
        dbconnector.close_connection()
    else:
        if file_index is None:
            infile = io.open(db_name, 'r', encoding='utf8')
            for line in infile.readlines():
                data = line.split("|")
                file_index[data[0]] = data[1]
        for term in terms:
            search_results[term] = file_index[term]
    return search_results




