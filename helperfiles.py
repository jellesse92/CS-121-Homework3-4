# -*- coding: utf-8 -*-
from collections import defaultdict
import csv
import re
import math
import dbconnector
import ast

#DATABASE MODE VS Print to File
DB_MODE = True

def get_tfidf(indexdict, n):
    tfidf = defaultdict(list)
    errors = []
    if DB_MODE:
        dbconnector.build_connection()
    for term, value in indexdict.items():
        for pair in value:
            tf_idf = calculate_tfidf(pair[1], n / len(indexdict[term]))
            ranking = rank_important_words(tf_idf, pair[2])
            tfidf[term].append((pair[0], float(round(ranking, 2, )), str(pair[2]), str(pair[3])))
        try:
            if not DB_MODE:
                write_row_db(str(term), tfidf[term])
            else:
                dbconnector.insert_data(term, str(tfidf[term]))
        except Exception as e:
            errors.append( "Failed to write entry for Term: " + str(term) + "And Value" + str(value))
            print (errors[-1])

    if DB_MODE:
        # dbconnector.build_connection()
        # dbconnector.insert_all_data(tfidf)
        dbconnector.close_connection()
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
        calculation = calculation * additional_ranking
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
    outfile = open("temporarydatabase.tsv", "a+", encoding='utf8')
    writer = csv.writer(outfile, delimiter='\t',)
    writer.writerow(index_values)
    outfile.close()
    return


def get_tokens(text):
    tokens = defaultdict(int)
    text = re.sub(r'[^\w\s]',' ',text)
    for word in text.lower().strip().split():
        tokens[word] += 1
    return tokens


def query_terms(*terms) -> str:
    if DB_MODE:
        dbconnector.build_connection()
        search_results = defaultdict(list)
        for term in terms:
            search_results[term] = ast.literal_eval(dbconnector.query_data(term))
        return search_results
        dbconnector.close_connection()
    else:
        # QUERY AGAINST FILE
        print("Not Implemented Yet")


