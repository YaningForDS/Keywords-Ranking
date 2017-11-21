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
from pyexcel_xls import get_data
import json
import matplotlib.pyplot as plt

reload(sys) 
sys.setdefaultencoding('utf8')

current_file_path = __file__
foldername = os.path.dirname(os.path.realpath(__file__))
stemmer = PorterStemmer()

##weighted frequency = frequency/wordcount
class text_visual():
	def main(self):
		print ('start working...')
		# data_dir = os.path.join(foldername, 'dictionary_terms.xlsx')
		# data = get_data(data_dir)
		# jsondata = json.dumps(data)
		# jsondata = jsondata[105:-3]
		# data_list = jsondata.split('],')
		# print data_list
		# newlist = []
		# for line in data_list:
		# 	line = line.split(',')[0].replace('"','').replace('[','').strip()
		# 	newlist.append(line)
		newlist = ['regard wtoinconsist','inconsist fair','concept fair', 'proceed inconsist', 'norm gener',
					'stare decisi', 'rule norm', 'creat legitim', 'basi oblig', 'held inconsist', 'requir fair',
					'impos unreason', 'read oblig', 'evenhand', 'expect wto','legal rule', 'investig violat',
					'order inconsist', 'unbias object','appli inconsist', 'interpret legal', 'result inconsist',
					'central element', 'disput inconsist', 'bodi jurisprud', 'function wto', 'practic inconsist',
					'wtoinconsist measur', 'violat relev', 'textual basi', 'materi injur', 'interpret relev',
					'inconsist certain','textual analysi', 'interpret public','legal question','establish oblig']
		cv = CountVectorizer(vocabulary=newlist,ngram_range=(2, 2))
		set_B_case_pre, set_B_case_dict = self.convert_B_to_caseslist(foldername)
		set_B_case = set_B_case_pre.values()
		case_name = set_B_case_pre.keys()
		vect = CountVectorizer(stop_words = 'english',ngram_range=(2, 2), decode_error='ignore',tokenizer = self.tokenize)
		res = {}
		for index in xrange(len(set_B_case)):
			case_B_name = case_name[index]
			doc = [set_B_case[index]]
			a = vect.fit_transform(doc)
			index,keys = self.key(vect)
			new_vocab = []
			for value in keys:
				value = value.encode('ascii')
				new_vocab.append(value)
			print len(new_vocab)
			newmatrix = cv.fit_transform(new_vocab)
			freq = newmatrix.sum()
			weighted_freq = (100*freq)/float(len(new_vocab))
			res[case_B_name] = weighted_freq
		return res
	def convert_A_to_list(self, foldername):
		data_dir = os.path.join(foldername, 'SET_A_txt_zeroing_cases')
		set_A = []
		for filename in os.listdir(data_dir):
			item = ''
			f = open(data_dir+'/'+filename,'r')
			item = f.read()
			f.close()
			item = item.replace('\n','')
			#item = item.encode('utf-8').strip()
			set_A.append(item)
		set_A = [doc.replace(b"<br />", b" ") for doc in set_A]
		return set_A

	def convert_B_to_caseslist(self, foldername):
		data_dir = os.path.join(foldername, 'SET_B_subsidies')
		set_B_case_dict = {}
		set_B_case_list = {}
		test_set = set()
		i = 1
		pre_file = ''
		counter = 0
		case = ''
		current_file_name = 'WTDS46'
		for filename in os.listdir(data_dir):
			if filename != '.DS_Store':
				item = ''
				pre_file = filename.split('-')[0]
				test_set.add(pre_file)
				f = open(data_dir+'/'+filename,'r')
				item = f.read()
				f.close()
				if len(test_set) == i:
					case = case + item
					counter = counter + 1
				else:
					set_B_case_list[current_file_name] = case
					set_B_case_dict[current_file_name] = counter
					current_file_name = pre_file
					i = i + 1
					case = ''
					case = case + item
					counter = 1
		if case != '':
			set_B_case_list[pre_file] = case
			set_B_case_dict[pre_file] = counter
			#print counter, len(set_A_case_list), len(test_set)
		return set_B_case_list, set_B_case_dict

	def stem_tokens(self, tokens, stemmer):
	    stemmed = []
	    for item in tokens:
	        stemmed.append(stemmer.stem(item))
	    return stemmed

	def tokenize(self, text):
	    text = "".join([ch for ch in text if ch not in string.punctuation])
	    tokens = nltk.word_tokenize(text)
	    stems = self.stem_tokens(tokens, stemmer)
	    return stems

	def key(self, vect):
		dic = vect.vocabulary_
		sorted_x = OrderedDict(sorted(dic.items(), key=lambda t: t[1]))
		index = sorted_x.values()
		keys = sorted_x.keys()
		return index, keys

o = text_visual()
myDictionary = o.main()
print myDictionary
#width = 1
#plt.bar(myDictionary.keys(), myDictionary.values(), width, color='g')