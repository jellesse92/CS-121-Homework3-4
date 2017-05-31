# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:51:38 2017

@author: aisha
"""


#tokenize  informatics – doc_1, 5 ; doc_2, 10 ; doc_3, 7
from collections import defaultdict
import json
from bs4 import BeautifulSoup
import PartA
import nltk 
import pickle
import os
import math



def SaveObject(objectToSave, filename):
   
    with open(filename + '.pickle', 'wb') as handle:
        pickle.dump(objectToSave, handle, protocol=pickle.HIGHEST_PROTOCOL)

def LoadObject(filename):
    if(os.path.exists(filename + '.pickle')):
        with open(filename + '.pickle', 'rb') as handle:
            return pickle.load(handle)
    else:
        print("File does not exist")


def TfidfDict(): 
    
    frequency_dict = defaultdict(list)
    tfidf_dict = defaultdict(list)
    total_documents = 0
    with open('bookkeeping.json') as data_file:    
        data = json.load(data_file)
    for location, url_link in data.items():
        unique_words = defaultdict(list)
        total_documents += 1
        grab_location = location.split('/')
        open_file = "C:\\Users\\aisha\\OneDrive\\Documents\\CS121\\Assignment4\\webpages_clean\\WEBPAGES_CLEAN" + "\\" + grab_location[0] + "\\" + grab_location[1]   
        html = open(open_file, 'r', encoding="utf8")
        soup = BeautifulSoup(html, 'html.parser')
        unique_words = ImportantWords(soup, unique_words)
        grab_text = soup.get_text()
        tokenize_txt = PartA.tokenize(grab_text)
        freq_word = nltk.FreqDist(tokenize_txt).most_common()
        for words, freq in freq_word: 
            if words in unique_words:
                frequency_dict[words].append((url_link, freq, unique_words[words]))
            else: 
                frequency_dict[words].append((url_link, freq))
    for word, items in frequency_dict.items():
            for x in range(len(items)): 
                if len(items[x]) == 2: 
                    i = items[x] 
                    calculate = (1 + math.log10(i[1])) * (math.log10(total_documents / len(items)))
                    tfidf_dict[word].append((i[0], str(round(calculate, 2))))
                elif len(items[x]) == 3: 
                    i = items[x] 
                    calculate = (1 + math.log10(i[1])) * (math.log10(total_documents / len(items)))
                    tfidf_dict[word].append((i[0], str(round(calculate, 2)), i[2])) 
            
    return tfidf_dict
            

def ImportantWords(soup, unique_words): 
    if soup.find('b') != None: 
        txt = soup.find('b').text 
        token = PartA.tokenize(txt)
        for w in token: 
            unique_words[w].append("b")
    if soup.find('h1') != None: 
        txt = soup.find('h1').text 
        token = PartA.tokenize(txt)
        for w in token: 
            unique_words[w].append("h1")
    if soup.find('h2') != None: 
        txt = soup.find('h2').text 
        token = PartA.tokenize(txt)
        for w in token: 
            unique_words[w].append("h2")
    if soup.find('h3') != None: 
        txt = soup.find('h2').text 
        token = PartA.tokenize(txt)
        for w in token: 
            unique_words[w].append("h3")
    return unique_words
    
    
        
#tfidf_dict = TfidfDict()
#SaveObject(tfidf_dict, "saved_dictionary.txt")
saved_dict = LoadObject("saved_dictionary.txt")
#print(len(saved_dict))
#file_obj = open("url_query.txt", 'w')
#vals = saved_dict["informatics"]
#file_obj.write("INFORMATICS: \n")
#for (x, y) in vals: 
#    file_obj.write(x)
#    file_obj.write("\n")
#
#file_obj.write("\nMONDEGO: \n")   
#G = saved_dict["mondego"]
#for (x, y) in G: 
#    file_obj.write(x)
#    file_obj.write("\n")
#    
#T = saved_dict["irvine"]
#file_obj.write("\nIRVINE: \n")
#for (x, y) in T: 
#    file_obj.write(x)
#    file_obj.write("\n")
#
#file_obj.close()




def Prompt(saved_dict): 
    user_input = input("Enter query:")
    
    

