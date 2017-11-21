import os
import csv
import spacy
import nltk
import sys
from operator import itemgetter
from collections import OrderedDict
from scipy import sparse
from scipy.sparse import *
from scipy import *
import numpy as np
from numpy import array
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer
import string
from sklearn.feature_extraction.text import CountVectorizer
import codecs

reload(sys)  
sys.setdefaultencoding('utf8')

current_file_path = __file__
foldername = os.path.dirname(os.path.realpath(__file__))
stemmer = PorterStemmer()
print stemmer.stem('america laws')
print stemmer.stem('00 1265')

sen = ['america laws','law']

def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed

def tokenize(text):
    text = "".join([ch for ch in text if ch not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems
# cv = CountVectorizer(ngram_range=(2, 2),stop_words = 'english',decode_error='ignore',tokenizer = tokenize)
# a = cv.fit_transform(sen)
cv1 = CountVectorizer(ngram_range=(1, 2),stop_words = 'english',decode_error='ignore')
a1 = cv1.fit_transform(sen)
# alist = cv.get_feature_names()
# ## alist_final after tokenized 
# alist_final = [x.encode('UTF8') for x in alist]
# 'incomplet': ['stemmed incomplete']

blist = cv1.get_feature_names()
blist_final = [x.encode('UTF8') for x in blist]
print blist_final
sample_dict = {'law':0,'stem':1}
#cvv = CountVectorizer(ngram_range=(1, 2),stop_words = 'english',decode_error='ignore',tokenizer = tokenize)
#c = cvv.fit_transform(blist_final)
#single_token_list =  cvv.get_feature_names()
#single_token =  [y.encode('UTF8') for y in single_token_list]
#print single_token
for j in blist_final:
	item = stemmer.stem(j)
	#for item in single_token:
	if item in sample_dict:
		if type(sample_dict[item]) == int:
			sample_dict[item] = [j]
		else:
			if sample_dict[item] != [j]:
				sample_dict[item] += [j]
# cvv = CountVectorizer(ngram_range=(1, 2),stop_words = 'english',decode_error='ignore',tokenizer = tokenize)
# c = cvv.fit_transform(sen)
# single_token_list =  cvv.get_feature_names()
# single_token =  [y.encode('UTF8') for y in single_token_list]
# ##single_token is key, blist_final is value
# map_dict = dict(zip(single_token, blist_final))

# for item in map_dict:
# 	if item in sample_dict:
# 		sample_dict[item] = map_dict[item]
# #print single_token
# print map_dict
print sample_dict
# for j in blist_final:
# 	for item in single_token:
# 		#print item
# 		if item in sample_dict:
# 			if type(sample_dict[item]) == int:
# 				sample_dict[item] = [j]
# 			else:
# 				sample_dict[item] += [j]
	#print single_token
	# break
#print sample_dict
	



#print alist_final
#print blist_final