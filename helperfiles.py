# -*- coding: utf-8 -*-
from collections import defaultdict
import csv
import re
import math


def get_tfidf(indexdict, df, n):
    tfidf = defaultdict(list)
    errors = []
    for term, value in indexdict.items():
        for pair in value:
            if len(pair) == 2:
                tfidf[term].append((pair[0], calculate_tfidf(pair[1], n / len(indexdict[term]))))
            else:
                tfidf[term].append((pair[0], calculate_tfidf(pair[1], n / len(indexdict[term]))))
        try:
            write_row_db(str(term), tfidf[term])
        except Exception as e:
            errors.append( "Failed to write entry for Term: " + str(term) + "And Value" + str(value) + e.reason)
            print (errors[-1])
    return tfidf, errors


def calculate_tfidf(tf, idf):
    return (1 + math.log10(tf)) * math.log10(idf)


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



