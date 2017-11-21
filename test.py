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
data_dir = os.path.join(foldername, 'SET_A_txt_zeroing_cases')
set_A_case_dict = {}
set_A_case_list = []
test_set = set()
i = 1
pre_file = ''
counter = 0
case = ''
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
		set_A_case_list.append(case)
		set_A_case_dict[pre_file] = counter
		i = i + 1
		case = ''
		case = case + item
		counter = 1
if case != '':
	set_A_case_list.append(case)
#print len(set_A_case_list), len(test_set)
#print test_set


def convert_A_to_caseslist(foldername):
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
	return set_A_case_list.keys(), set_A_case_dict

a, b = convert_A_to_caseslist(foldername)
print a,b.values()
print b

filedname2 = ["Stemmed Term"]	#column_number = len(set_A)print b
for i in xrange(len(a)):
	print i
	case = ''
	case = 'Case A-{} DocFreq'.format(i+1)
	filedname2.append(case)

print filedname2
