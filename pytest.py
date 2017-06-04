#!/usr/bin/env python

""".

pytest.py

    Author  :   Helio Tejeda
    Date    :   01 June 2017

Simple python test to see if php will execute it.


from sys import argv as cla


h = ['a', 'b', 'c', 'd']
print 'this is a test'
print 'somthing else'
for i in h:
    print i

print cla[1]
"""

""".

execute_query.py

    Author(s)   :   Aisha
                    Helio
                    Jasmine
    Date        :   01 June 2017

Python script to execute user queries
"""

# from __future__ import print_function
from sys import argv as cla

from dbconnector import query_data
from dbconnector import query_urls

#from requests import get
#from lxml.html import fromstring

# if __name__ == '__main__':
# print("HERE1")
terms = cla[1:]

# To be used when ther is an overlap between different terms
union_output = []
traversed_docs = set()
traversed_doc_scores = dict()
union_docs = set()
union_doc_scores = dict()
final_output = []
for t in terms:
    #print t
    #print ''
    this_term_output = []
    output = query_data(t)
    #print output
    #print ''

    for doc, tfidf in output:
        if ('//' in doc):
            doc = doc.replace('//', '/')

        # Get url for the doc
        this_location = query_urls(doc)

        # If we have already seen this doc, then we can add it to the union set
        if (doc in traversed_docs):
            union_docs.add(doc)
            if (doc in union_doc_scores):
                union_doc_scores[doc] += tfidf
            else:
                union_doc_scores[doc] = traversed_doc_scores[doc] + tfidf

            union_output.append((
                union_doc_scores[doc], doc, this_location
            ))
        else:
            this_term_output.append((tfidf, doc, this_location))

            # Add doc to traversed docs
            traversed_docs.add(doc)
            # Add score to traversed only if it is not already in union
            traversed_doc_scores[doc] = tfidf

    this_term_output.sort(key=lambda tup: tup[0], reverse=True)
    final_output.extend(this_term_output)

#print 'OUTPUTS\n'
#print 'UNION:\n'
#print union_output
#print len(union_output)
#print 'INDIVID:\n'
#print final_output
#print len(final_output)
#print '\n\n'
# First print out the union, since together they are higher quality
union_output.sort(key=lambda tup: tup[0], reverse=True)
for score, doc, url in union_output:
    print str(score) + ",X," + doc + ",X," + url
    # print()

# Order the rankings from high tfidf to low tfidf
final_output.sort(key=lambda tup: tup[0], reverse=True)
for score, doc, url in final_output:
    if (doc not in union_docs):
        print str(score) + ",X," + doc + ",X," + url
        # print()
