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

class text_analysis():
	def __init__(self):
		self.csvfile1 = codecs.open('sheet1.csv','w',encoding = 'utf-8')
		self.csvfile2 = codecs.open('sheet2_B.csv','w',encoding = 'utf-8')
		self.fieldnames1 = ['Stemmed Term', 'Set A occurences', 'Set B occurences', 'ratio DocFreq(A) to DocFreq(B)']
		self.writer1 = csv.DictWriter(self.csvfile1,fieldnames=self.fieldnames1)
		self.writer1.writeheader()

	def main(self):
		print('start working...')
		set_A = self.convert_A_to_list(foldername)
		set_B = self.convert_B_to_list(foldername)
		set_A_case_pre, set_A_case_dict = self.convert_A_to_caseslist(foldername)
		set_B_case_pre, set_B_case_dict = self.convert_B_to_caseslist(foldername)
		set_A_case = set_A_case_pre.values()
		set_B_case = set_B_case_pre.values()
		vect = CountVectorizer(min_df = 10, stop_words = 'english',decode_error='ignore',tokenizer = self.tokenize)
		sparse_matrix_A = vect.fit_transform(set_A)
		sparse_matrix_B = vect.transform(set_B)
		sparse_matrix_A_cases = vect.transform(set_A_case)
		print shape(sparse_matrix_A)
		print shape(sparse_matrix_B)
		print shape(sparse_matrix_A_cases)
		print("Vocabulary size: {}".format(len(vect.vocabulary_)))
		t_A = sparse_matrix_A.nonzero()
		sparse_matrix_A[t_A] = 1
		t_B = sparse_matrix_B.nonzero()
		sparse_matrix_B[t_B] = 1
		t_A_case = sparse_matrix_A_cases.nonzero()
		sparse_matrix_A_cases[t_A_case] = 1
		
		res_vector_A = sparse_matrix_A.sum(axis = 0)
		res_vector_B = sparse_matrix_B.sum(axis = 0)
		index, keys = self.key(vect)
		print len(keys)
		for index in xrange(len(keys)):
			stem = keys[index]
			A_DocFreq = float(res_vector_A[0,index])/len(set_A)
			B_DocFreq = float(res_vector_B[0,index])/len(set_B)
			if B_DocFreq == 0:
				ratio = 'inf'
			else:
				ratio = A_DocFreq/float(B_DocFreq)
			self.writer1.writerow({'Stemmed Term': stem, 'Set A occurences': A_DocFreq, 'Set B occurences': B_DocFreq, 'ratio DocFreq(A) to DocFreq(B)': ratio})
		
		print('sheet2 working...')
		filedname2 = ["Stemmed Term"]
		#column_number = len(set_A)
		case_name = set_A_case_pre.keys()
		for i in xrange(len(set_A_case)):
			case = ''
			case = 'Case A-{} DocFreq'.format(case_name[i])
			filedname2.append(case)
		writer2 = csv.DictWriter(self.csvfile2, fieldnames = filedname2)
		writer2.writeheader() 
		
		number_of_docs = set_A_case_dict.values()
		print len(number_of_docs)
		for j in xrange(len(keys)):
		#for j in xrange(5):
			stems = keys[j]
			new_dict = {'Stemmed Term': stems}
			print new_dict
			w = sparse_matrix_A_cases.getcol(j).toarray()
			print len(w)
			for v in xrange(len(w)):
				new_key = ''
				new_key = 'Case A-{} DocFreq'.format(case_name[v])
				new_dict[new_key] = w[v,0]/float(number_of_docs[v])
			print new_dict
			writer2.writerow(new_dict)

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
		return set_A_case_list, set_A_case_dict

	def convert_A_to_caseslist(self, foldername):
		data_dir = os.path.join(foldername, 'SET_A_txt_zeroing_cases')
		set_A_case_dict = {}
		set_A_case_list = {}
		test_set = set()
		i = 1
		pre_file = ''
		counter = 0
		case = ''
		current_file_name = 'WTDS179'
		for filename in os.listdir(data_dir):
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
				set_A_case_list[current_file_name] = case
				set_A_case_dict[current_file_name] = counter
				current_file_name = pre_file
				i = i + 1
				case = ''
				case = case + item
				counter = 1
		if case != '':
			set_A_case_list[pre_file] = case
			set_A_case_dict[pre_file] = counter
			#print counter, len(set_A_case_list), len(test_set)
		return set_A_case_list, set_A_case_dict

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

	def convert_B_to_list(self, foldername):
		data_dir = os.path.join(foldername,'SET_B_subsidies')
		set_B = []
		for filename in os.listdir(data_dir):
			item = ''
			f = open(data_dir+'/'+filename,'r')
			item = f.read()
			f.close()
			item = item.replace('/n','')
			#item = item.encode('utf-8').strip()
			set_B.append(item)
		set_B = [doc.replace(b"<br />", b" ") for doc in set_B]
		return set_B
#stemmer = PorterStemmer()
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

o = text_analysis()
o.main()
# def stem_tokens(self, tokens, stemmer):
#     stemmed = []
#     for item in tokens:
#         stemmed.append(stemmer.stem(item))
#     return stemmed


# def tokenize(self, text):
#     tokens = nltk.word_tokenize(text)
#     tokens = [i for i in tokens if i not in string.punctuation]
#     stems = self.stem_tokens(stemmer, tokens)
#     return stems

# # set_A = convert_A_to_list(foldername)
# # set_B = convert_B_to_list(foldername)
# set_A = ['The swimmer likes swimming so he swims.']
# vect = CountVectorizer(min_df = 1, stop_words = 'english',decode_error='ignore',tokenizer = tokenize)

# # sparse_matrix_A = vect.fit_transform(set_A)
# # sparse_matrix_B = vect.transform(set_B)
# print("Vocabulary size: {}".format(len(vect.vocabulary_)))
# #print("Vocabulary content:\n {}".format(vect.vocabulary_))
# print type(sparse_matrix_A)
# res_vector_A = sparse_matrix_A.sum(axis = 0)
# res_vector_B = sparse_matrix_A.sum(axis = 0)
# print len(res_vector)
# #bag_of_words = vect.transform
# import csv
# csvfile = open('mycsv.csv','w')
# fieldnames = ['Stemmed Term', 'Set A occurences', 'Set B occurences', 'ratio DocFreq(A) to DocFreq(B)']
# writer = csv.DictWriter(csvfile,fieldnames=self.fieldnames)
# writer.writeheader()
# for index in xrange(len(keys)):
# 	stem = keys[index]
# 	A_DocFreq = res_vector_A[0,index]
# 	B_DocFreq = res_vector_B[0,index]
# 	ratio = A_DocFreq/float(B_DocFreq)
# 	writer.writerow({'Stemmed Term': stem, 'Set A occurences': A_DocFreq, 'Set B occurences': B_DocFreq, 'ratio DocFreq(A) to DocFreq(B)': ratio})




