#!/usr/bin/env python

""".

execute_query.py

    Author(s)   :   Aisha
                    Helio
                    Jasmine
    Date        :   01 June 2017

Python script to execute user queries
"""

from __future__ import print_function
from sys import argv as cla

from dbconnector import query_data
from dbconnector import query_urls

from requests import get
from lxml.html import fromstring

# if __name__ == '__main__':
print("HERE1")
terms = cla[1:]
output = query_data(terms[0])
print("HERE")
# print(type(output))
# print(output)
final_output = []
for doc, tfidf in output:
    if ('//' in doc):
        doc = doc.replace('//', '/')
    # print(doc)
    this_location = query_urls(doc)
    # print(type(this_location))
    # print(this_location)
    # print()
    try:
        req = get('http://' + str(this_location))
        # print(req)
        tree = fromstring(req.content)
        # print(tree.findtext('.//title'))
        title = tree.findtext('.//title')
        final_output.append((tfidf, doc, this_location, title))
    except:
        final_output.append((tfidf, doc, this_location, 'Title Not Found'))

"""
print(final_output)
for i, j, k, l in final_output:
    print(i)
    print(j)
    print(k)
    print(l)
    print()
"""
final_output.sort(key=lambda tup: tup[0], reverse=True)
"""
for i, j, k, l in final_output:
    print(i)
    print(j)
    print(k)
    print(l)
    print()
"""
for score, doc, url, title in final_output:
    print(str(score) + ",X, " + doc + ",X, " + url + ",X, " + title)
    # print()
