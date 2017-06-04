# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:51:38 2017

@author: aisha
"""
import mysql.connector

#tokenize  informatics – doc_1, 5 ; doc_2, 10 ; doc_3, 7
from collections import defaultdict
import json
from bs4 import BeautifulSoup
import PartA
import nltk 
#import pickle
#import os
import math
import re
#from pymongo import MongoClient 




def tokenize(file):
    """Remove punctuation using regex (sequence of characters 
    that define a search pattern), ^\w\s (replace everything but word character and whitespace)
    returns a list of words after removing punctuation and lower casing words""" 
    sentence = ""
    
    for line in file:
        sentence += re.sub(r'[^\w\s]',' ',line)
        
    return sentence.lower().strip().split()
    


def TfidfDict(): 
    """This function returns the tfidf dictionary
        {word: (docID, tfidf, [list of tags], [list of positions])}
        list of tags includes 't' for title, b, h1, h2, h3 
                    (may be empty if tags are not present)
        list of positions = all the positions the word is in the doc  
        """
    frequency_dict = defaultdict(list)
    tfidf_dict = defaultdict(list)
    total_documents = 0
    with open('bookkeeping.json') as data_file:    
        data = json.load(data_file)
    for location, url_link in data.items():
        imp_words = defaultdict(list)
        total_documents += 1
        html = open(str(location), 'r', encoding="utf8")
        soup = BeautifulSoup(html, 'lxml')
        imp_words = ImportantWords(soup, imp_words)
        grab_text = soup.get_text()
        tokenize_txt = tokenize(grab_text)
        freq_word = nltk.FreqDist(tokenize_txt).most_common()
        for words, freq in freq_word:
            insert_position = [w.start() for w in re.finditer(words, soup.get_text())]
            frequency_dict[words].append((str(location), freq, imp_words[words], insert_position))
    for word, items in frequency_dict.items():
        for info in range(len(items)): 
            i = items[info]
            calculate = (1 + math.log10(i[1])) * (math.log10(total_documents / len(items)))
            calculation = RankImportantWords(calculate, i[2])
            tfidf_dict[word].append((i[0], float(round(calculation,2)), i[2], i[3])) 
      

    return tfidf_dict 
    

    
def RankImportantWords(calculation, imp_list): 
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
        
    
def ImportantWords(soup, unique_words):
    """This function is called in TfidfDict()
       Its parameters include parsed text data and an empty dictionary
       
       soup: document text
       unique_words: empty dictionary 
       
       finds t (title), b, h1, h2, h3 tags in the doc and 
       associates it to the word"""
       
    
    titles = soup.find('body')
    if titles != None: 
        titles = titles.findAll(text=True, recursive=True)
        
    if titles != None and len(titles) > 1: 
        token = tokenize(titles[0])
        for w in token:
            unique_words[w].append("t")
    if soup.find('b') != None: 
        txt = soup.find('b').text 
        token = tokenize(txt)
        for w in token: 
            unique_words[w].append("b")
    if soup.find('h1') != None: 
        txt = soup.find('h1').text 
        token = tokenize(txt)
        for w in token: 
            unique_words[w].append("h1")
    if soup.find('h2') != None: 
        txt = soup.find('h2').text 
        token = tokenize(txt)
        for w in token: 
            unique_words[w].append("h2")
    if soup.find('h3') != None: 
        txt = soup.find('h2').text 
        token = tokenize(txt)
        for w in token: 
            unique_words[w].append("h3")
    return unique_words
    

    


#tfidf = TfidfDict()





























    
    

