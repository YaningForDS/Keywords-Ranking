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


mapping = {'central element': ['central element'], 'wtoinconsist measur': ['wto inconsist measure'], 
'basi oblig': ['basis obligations'], 'read oblig': ['read obligation', 'read obligations'], 
'violat relev': ['violations relevant'], 'concept fair': ['concept fair', 'concept fairness'], 
'order inconsist': ['order inconsistent'], 'establish oblig': ['establish obligation', 'establish obligations'], 
'legal rule': ['legal rulings'], 'evenhand': ['evenhanded'], 'function wto': ['function wto'], 'stare decisi': ['stare decisis'], 
'creat legitim': ['creating legitimate'], 'expect wto': ['expect wto'], 'textual analysi': ['textual analysis'], 
'requir fair': ['requiring fair'], 'materi injur': ['materially injuring'], 'investig violat': ['investigations violations'], 
'practic inconsist': ['practices inconsistent'], 'legal question': ['legal questions'], 'bodi jurisprud': ['body jurisprudence'], 
'appli inconsist': ['applied inconsistent'], 'inconsist fair': ['inconsistently fair'], 'disput inconsist': ['disputes inconsistent'], 
'interpret relev': ['interpret relevant'], 'impos unreason': ['imposing unreasonable'], 'interpret public': ['interpretation public'], 
'rule norm': ['rule norm', 'rule normal', 'rule normally', 'rule normative'], 
'inconsist certain': ['inconsistently certain'], 'norm gener': ['norm general'], 'unbias object': ['unbiased objective'], 
'textual basi': ['textual basis'], 'result inconsist': ['result inconsistencies', 'result inconsistent'], 
'regard wtoinconsist': ['wto inconsistent'], 'interpret legal': ['interpreting legal'], 
'proceed inconsist': ['proceed inconsistency'], 'held inconsist': ['held inconsistency', 'held inconsistent']}

set_name = ['WTDS379-R-05', 'WTDS379-R-04', 'WTDS379-R-07', 'WTDS379-R-06', 'WTDS379-R-01', 'WTDS59-4', 'WTDS379-R-03', 'WTDS379-R-02', 'WTDS330-1', 'WTDS257-14', 'WTDS222-10', 'WTDS353-9', 'WTDS357-11', 'WTDS357-10', 'WTDS311-1', 'WTDS70-8', 'WTDS311-2', 'WTDS145-1', 'WTDS316-12R1', 'WTDS412-14 2', 'WTDS257-6', 'WTDS257-7', 'WTDS257-4', 'WTDS257-5', 'WTDS257-2', 'WTDS257-3', 'WTDS412-17 2', 'WTDS257-1', 'WTDS283-10 3', 'WTDS283-10 2', 'WTDS257-8', 'WTDS257-9', 'WTDS295-11C1', 'WTDS128-1', 'WTDS311-2-add.1', 'WTDS310-2', 'WTDS70-3', 'WTDS54-17A1 3', 'WTDS138-R-00', 'WTDS70-4', 'WTDS70-5', 'WTDS316-R-06', 'WTDS283-4 3', 'WTDS221-4', 'WTDS301-R', 'WTDS59-3', 'WTDS234-17', 'WTDS234-16', 'WTDS142-12 (2)', 'WTDS234-14', 'WTDS234-13', 'WTDS234-12', 'WTDS106-1', 'WTDS234-10', 'WTDS316-6', 'WTDS316-7', 'WTDS212-9', 'WTDS212-8', 'WTDS316-2', 'WTDS265-36', 'WTDS234-19', 'WTDS234-18', 'WTDS336-4', 'WTDS336-5', 'WTDS336-6', 'WTDS336-7', 'WTDS336-1', 'WTDS296-11', 'WTDS296-10', 'WTDS388-10', 'WTDS336-8', 'WTDS336-9', 'WTDS339-8', 'WTDS339-3', 'WTDS339-2', 'WTDS339-1', 'WTDS339-7', 'WTDS339-6', 'WTDS339-5', 'WTDS339-4', 'WTDS388-3', 'WTDS234-18 2', 'WTDS427-R', 'WTDS127-1', 'WTDS426-18', 'WTDS222-7C1', 'WTDS426-16', 'WTDS426-15', 'WTDS283-9 2', 'WTDS283-9 3', 'WTDS426-10', 'WTDS295-13A1', 'WTDS316-R-05', 'WTDS357-8', 'WTDS345-R-03', 'WTDS388-5', 'WTDS296-7', 'WTDS277-1', 'WTDS277-2', 'WTDS277-3', 'WTDS277-4', 'WTDS277-5', 'WTDS277-6', 'WTDS277-7', 'WTDS212-R', 'WTDS316-14', 'WTDS353-13', 'WTDS353-12', 'WTDS353-11', 'WTDS353-10', 'WTDS336-12', 'WTDS336-10', 'WTDS336-11', 'WTDS234-7', 'WTDS234-6', 'WTDS234-5', 'WTDS234-4', 'WTDS234-3', 'WTDS234-2', 'WTDS234-1', 'WTDS234-11', 'WTDS234-8', 'WTDS353-R-01', 'WTDS316-15', 'WTDS379-12A1', 'WTDS345-ABR', 'WTDS139-3 2', 'WTDS353-R-03', 'WTDS353-R-02', 'WTDS310-1', 'WTDS234-15 2', 'WTDS54-16 3', 'WTDS353-R-05', 'WTDS70-R', 'WTDS353-R-04', 'WTDS273-4', 'WTDS273-5', 'WTDS257-R-04', 'WTDS273-7', 'WTDS257-R-02', 'WTDS257-R-03', 'WTDS257-R-00', 'WTDS257-R-01', 'WTDS353-R-06', 'WTDS145-1R1', 'WTDS213-1-add-1', 'WTDS59-1', 'WTDS59-5', 'WTDS267-RA1-01', 'WTDS139-11 2', 'WTDS414-RA1', 'WTDS234-16 2', 'WTDS138-3c1', 'WTDS358-2', 'WTDS358-3', 'WTDS358-4', 'WTDS358-5', 'WTDS358-6', 'WTDS358-7', 'WTDS358-8', 'WTDS358-9', 'WTDS52-2', 'WTDS299-8', 'WTDS167-1', 'WTDS167-2', 'WTDS353-7', 'WTDS353-6', 'WTDS353-5', 'WTDS353-4', 'WTDS299-1', 'WTDS299-2', 'WTDS299-3', 'WTDS299-4', 'WTDS299-5', 'WTDS299-6', 'WTDS299-7', 'WTDS103-12A6', 'WTDS103-12A5', 'WTDS103-12A4', 'WTDS103-12A3', 'WTDS103-12A2', 'WTDS103-12A1', 'WTDS266-21', 'WTDS266-20', 'WTDS266-27', 'WTDS277-20-add.1', 'WTDS357-9', 'WTDS138-9C1', 'WTDS357-7', 'WTDS357-6', 'WTDS357-5', 'WTDS357-4', 'WTDS357-3', 'WTDS317-1-add.1', 'WTDS357-1', 'WTDS317-3', 'WTDS317-2', 'WTDS317-1', 'WTDS379-12A3', 'WTDS379-12A4', 'WTDS317-6', 'WTDS317-5', 'WTDS317-4', 'WTDS314-1', 'WTDS54-8 2', 'WTDS54-8 3', 'WTDS347-1', 'WTDS412-18', 'WTDS54-RC1 2', 'WTDS283-4 2', 'WTDS354-1', 'WTDS354-2', 'WTDS194-2', 'WTDS194-3', 'WTDS194-1', 'WTDS194-4', 'WTDS54-15', 'WTDS359-9', 'WTDS359-8', 'WTDS359-5', 'WTDS359-4', 'WTDS359-7', 'WTDS347-7', 'WTDS359-1', 'WTDS359-3', 'WTDS359-2', 'WTDS380-1', 'WTDS54-9', 'WTDS267-RA1-04', 'WTDS257-26', 'WTDS139-11', 'WTDS139-10', 'WTDS283-7 2', 'WTDS283-7 3', 'WTDS342-RA2', 'WTDS412-17A2', 'WTDS267-19', 'WTDS267-18', 'WTDS267-17', 'WTDS267-16', 'WTDS267-15', 'WTDS267-14', 'WTDS267-13', 'WTDS267-12', 'WTDS267-11', 'WTDS267-10', 'WTDS412-ABR', 'WTDS217-4A1', 'WTDS139-6 2', 'WTDS46-12', 'WTDS342-12 3', 'WTDS342-12 2', 'WTDS54-RC2 3', 'WTDS54-RC2 2', 'WTDS412-ABR 2', 'WTDS357-13', 'WTDS267-RC1', 'WTDS46-11', 'WTDS296-R-01', 'WTDS126-11', 'WTDS257-ABR', 'WTDS296-ABR', 'WTDS379-9', 'WTDS379-8', 'WTDS379-7', 'WTDS379-6', 'WTDS379-5', 'WTDS379-4', 'WTDS357-12', 'WTDS379-2', 'WTDS379-1', 'WTDS283-11 2', 'WTDS283-11 3', 'WTDS296-5', 'WTDS296-4', 'WTDS295-8', 'WTDS295-9', 'WTDS296-1', 'WTDS295-4', 'WTDS295-5', 'WTDS295-6', 'WTDS295-7', 'WTDS388-7', 'WTDS295-1', 'WTDS295-2', 'WTDS295-3', 'WTDS212-13', 'WTDS212-12', 'WTDS212-11', 'WTDS212-10', 'WTDS142-R 2', 'WTDS342-9 2', 'WTDS342-9 3', 'WTDS54-17 2', 'WTDS359-6', 'WTDS342-10', 'WTDS54-17A1 2', 'WTDS103-12', 'WTDS340-2', 'WTDS54-12 2', 'WTDS54-12 3', 'WTDS46-6', 'WTDS340-1', 'WTDS103-14', 'WTDS341-R-02', 'WTDS341-R-03', 'WTDS341-R-00', 'WTDS341-R-01', 'WTDS341-R-04', 'WTDS341-R-05', 'WTDS353-ABR', 'WTDS54-11', 'WTDS419-2', 'WTDS419-3', 'WTDS419-1', 'WTDS139-9 2', 'WTDS195-4', 'WTDS195-3', 'WTDS195-2', 'WTDS195-1', 'WTDS316-5A1', 'WTDS301-5', 'WTDS212-1-add-1', 'WTDS412-9', 'WTDS412-17A2 2', 'WTDS301-3', 'WTDS212-ABR', 'WTDS54-16', 'WTDS54-15 2', 'WTDS412-14', 'WTDS46-9', 'WTDS426-7 2', 'WTDS426-8', 'WTDS412-15 2', 'WTDS236-5-add.5', 'WTDS426-1-add.1', 'WTDS412-10', 'WTDS52-1', 'WTDS388-6', 'WTDS52-3', 'WTDS52-4', 'WTDS412-13', 'WTDS52-6', 'WTDS299-R-04', 'WTDS414-8', 'WTDS301-5C1', 'WTDS46-3', 'WTDS412-RA1', 'WTDS54-RC1 3', 'WTDS390-10', 'WTDS316-11', 'WTDS206-R-04', 'WTDS206-R-05', 'WTDS103-ABRC1', 'WTDS206-R-00', 'WTDS206-R-01', 'WTDS206-R-02', 'WTDS206-R-03', 'WTDS212-3', 'WTDS358-1-add.1', 'WTDS221-R', 'WTDS412-17A1', 'WTDS257-RC1', 'WTDS212-2', 'WTDS142-13', 'WTDS234-15', 'WTDS138-R-01', 'WTDS103-10', 'WTDS103-11', 'WTDS139-ABR', 'WTDS103-13', 'WTDS234-ABR', 'WTDS46-5', 'WTDS427-RA1', 'WTDS212-7', 'WTDS316-17', 'WTDS106-2', 'WTDS412-15', 'WTDS387-4', 'WTDS412-17', 'WTDS412-16', 'WTDS412-11', 'WTDS212-5', 'WTDS267-20', 'WTDS412-12', 'WTDS283-14 3', 'WTDS212-4', 'WTDS412-19', 'WTDS388-11', 'WTDS283-14 2', 'WTDS139-1', 'WTDS59-2', 'WTDS139-3', 'WTDS139-2', 'WTDS139-5', 'WTDS139-4', 'WTDS139-7', 'WTDS139-6', 'WTDS139-9', 'WTDS213-ABR', 'WTDS234-19 2', 'WTDS46-10', 'WTDS316-4', 'WTDS213-RC1', 'WTDS59-6', 'WTDS112-1', 'WTDS316-5', 'WTDS390-8', 'WTDS390-9', 'WTDS390-4', 'WTDS390-5', 'WTDS390-6', 'WTDS390-7', 'WTDS390-1', 'WTDS390-2', 'WTDS316-3', 'WTDS51-2', 'WTDS217-18', 'WTDS217-19', 'WTDS139-8', 'WTDS265-16', 'WTDS316-R-07', 'WTDS316-R-04', 'WTDS217-17', 'WTDS316-R-02', 'WTDS316-R-03', 'WTDS316-R-01', 'WTDS221-1', 'WTDS221-3', 'WTDS221-2', 'WTDS221-5', 'WTDS222-ARB', 'WTDS221-7', 'WTDS221-6', 'WTDS51-3', 'WTDS387-8', 'WTDS51-1', 'WTDS51-6', 'WTDS51-5', 'WTDS51-4', 'WTDS316-1', 'WTDS283-ABR', 'WTDS353-8', 'WTDS336-2', 'WTDS342-RA2 2', 'WTDS342-RA2 3', 'WTDS336-R', 'WTDS336-3', 'WTDS296-R-06', 'WTDS265-R', 'WTDS54-6C1', 'WTDS262-2', 'WTDS262-3', 'WTDS54-17 3', 'WTDS262-1', 'WTDS266-18', 'WTDS266-19', 'WTDS266-14', 'WTDS266-15', 'WTDS266-16', 'WTDS266-17', 'WTDS266-10', 'WTDS266-11', 'WTDS266-12', 'WTDS266-13', 'WTDS266-8', 'WTDS266-9', 'WTDS54-RC2', 'WTDS266-2', 'WTDS266-3', 'WTDS266-1', 'WTDS266-6', 'WTDS266-7', 'WTDS266-4', 'WTDS266-5', 'WTDS342-RA1-01-3', 'WTDS212-1', 'WTDS296-R-00', 'WTDS342-R-00 3', 'WTDS342-R-00 2', 'WTDS206-4', 'WTDS206-5', 'WTDS206-6', 'WTDS206-7', 'WTDS206-1', 'WTDS206-2', 'WTDS206-3', 'WTDS266-R', 'WTDS296-R-04', 'WTDS267-RA1-03', 'WTDS267-RA1-02', 'WTDS206-8', 'WTDS206-9', 'WTDS296-R-03', 'WTDS267-RA1-06', 'WTDS52-5', 'WTDS222-8', 'WTDS222-9', 'WTDS299-3C1', 'WTDS222-2', 'WTDS222-3', 'WTDS222-1', 'WTDS222-6', 'WTDS222-7', 'WTDS222-4', 'WTDS222-5', 'WTDS265-1', 'WTDS212-2A1', 'WTDS265-3', 'WTDS265-2', 'WTDS265-5', 'WTDS265-4', 'WTDS265-7', 'WTDS265-6', 'WTDS265-9', 'WTDS265-8', 'WTDS412-7', 'WTDS412-6', 'WTDS412-1', 'WTDS412-3', 'WTDS412-2', 'WTDS257-10', 'WTDS257-11', 'WTDS257-12', 'WTDS257-13', 'WTDS234-17 2', 'WTDS342-13 2', 'WTDS280-1', 'WTDS296-1-add.1', 'WTDS295-R-03', 'WTDS265-11', 'WTDS265-10', 'WTDS265-13', 'WTDS265-12', 'WTDS265-15', 'WTDS265-14', 'WTDS265-17', 'WTDS172-1', 'WTDS265-19', 'WTDS265-18', 'WTDS359-1-add.1', 'WTDS299-1-Rev.1', 'WTDS138-4', 'WTDS138-5', 'WTDS138-6', 'WTDS138-7', 'WTDS138-1', 'WTDS138-2', 'WTDS138-3', 'WTDS342-RA1-00 3', 'WTDS342-RA1-00 2', 'WTDS138-8', 'WTDS138-9', 'WTDS316-ABR', 'WTDS54-2', 'WTDS54-3', 'WTDS54-1', 'WTDS54-6', 'WTDS54-7', 'WTDS54-4', 'WTDS54-5', 'WTDS57-1', 'WTDS54-8', 'WTDS412-12 2', 'WTDS341-2', 'WTDS341-3', 'WTDS283-6 3', 'WTDS283-6 2', 'WTDS142-13 (2)', 'WTDS359-14', 'WTDS341-1', 'WTDS359-11', 'WTDS359-10', 'WTDS359-13', 'WTDS359-12', 'WTDS316-1-add.1', 'WTDS267-3', 'WTDS316-8A1', 'WTDS301-6', 'WTDS390-3', 'WTDS301-4', 'WTDS138-RC2', 'WTDS301-2', 'WTDS234-R-00 2', 'WTDS301-1', 'WTDS299-R-00', 'WTDS299-R-01', 'WTDS299-R-02', 'WTDS299-R-03', 'WTDS139-5 2', 'WTDS299-R-05', 'WTDS299-R-06', 'WTDS414-7', 'WTDS414-6', 'WTDS414-5', 'WTDS414-4', 'WTDS414-3', 'WTDS414-2', 'WTDS414-1', 'WTDS54-9 3', 'WTDS257-26-add.1', 'WTDS236-R-02', 'WTDS236-R-01', 'WTDS236-R-00', 'WTDS54-RC3 2', 'WTDS426-6R1', 'WTDS345-8', 'WTDS345-9', 'WTDS345-6', 'WTDS345-7', 'WTDS345-4', 'WTDS345-5', 'WTDS345-2', 'WTDS345-3', 'WTDS65-2', 'WTDS345-1', 'WTDS54-RC3 3', 'WTDS358-1', 'WTDS267-9', 'WTDS267-8', 'WTDS267-7', 'WTDS267-6', 'WTDS267-5', 'WTDS267-4', 'WTDS257-14A1', 'WTDS267-2', 'WTDS267-1', 'WTDS341-5', 'WTDS385-1', 'WTDS412-17A3 2', 'WTDS283-ABR 2', 'WTDS412-19 2', 'WTDS283-12 3', 'WTDS283-12 2', 'WTDS130-1', 'WTDS283-16A1', 'WTDS345-11', 'WTDS340-15', 'WTDS340-14', 'WTDS267-R', 'WTDS368-1', 'WTDS283-ABR 3', 'WTDS414-R', 'WTDS342-10 3', 'WTDS342-10 2', 'WTDS342-1', 'WTDS342-3', 'WTDS342-2', 'WTDS342-5', 'WTDS342-4', 'WTDS342-7', 'WTDS342-6', 'WTDS342-9', 'WTDS342-8', 'WTDS277-20', 'WTDS273-R-00', 'WTDS173-1', 'WTDS273-R-01', 'WTDS283-16 3', 'WTDS426-7', 'WTDS283-16 2', 'WTDS339-15', 'WTDS283-R', 'WTDS357-2', 'WTDS139-8 2', 'WTDS213-6', 'WTDS81-1', 'WTDS339-14', 'WTDS213-4', 'WTDS213-5', 'WTDS213-2', 'WTDS108-10', 'WTDS65-1', 'WTDS213-3', 'WTDS342-ABR', 'WTDS427-8', 'WTDS414-ABR', 'WTDS316-5A1 2', 'WTDS54-14 2', 'WTDS54-14 3', 'WTDS365-5', 'WTDS55-6', 'WTDS54-RC4 3', 'WTDS54-RC4 2', 'WTDS283-9', 'WTDS283-8', 'WTDS283-5', 'WTDS283-4', 'WTDS283-7', 'WTDS283-6', 'WTDS283-1', 'WTDS283-3', 'WTDS283-2', 'WTDS206-RC1', 'WTDS267-RA3-06', 'WTDS267-RA3-05', 'WTDS267-RA3-04', 'WTDS267-RA3-03', 'WTDS267-RA3-02', 'WTDS267-RA3-01', 'WTDS267-RA3-00', 'WTDS317-5A1C1 2', 'WTDS353-15', 'WTDS54-10', 'WTDS296-3', 'WTDS54-12', 'WTDS353-14', 'WTDS54-14', 'WTDS347-5', 'WTDS347-6', 'WTDS296-2', 'WTDS54-16 2', 'WTDS412-R', 'WTDS139-10 2', 'WTDS380-1-add.1', 'WTDS54-17A1', 'WTDS340-8', 'WTDS340-7', 'WTDS340-6', 'WTDS222-RC1', 'WTDS340-4', 'WTDS340-3', 'WTDS307-1', 'WTDS317-5A1', 'WTDS212-6', 'WTDS412-17A3', 'WTDS379-12A5', 'WTDS379-12A2', 'WTDS299-1-rev.1-add.1', 'WTDS222-R-02', 'WTDS222-R-03', 'WTDS222-R-00', 'WTDS222-R-01', 'WTDS296-9', 'WTDS388-8', 'WTDS283-15 2', 'WTDS296-8', 'WTDS283-15 3', 'WTDS358-12', 'WTDS358-13', 'WTDS358-10', 'WTDS358-11', 'WTDS358-14', 'WTDS108-1-add.1', 'WTDS54-7 2', 'WTDS365-1', 'WTDS365-2', 'WTDS365-3', 'WTDS365-4', 'WTDS234-9', 'WTDS365-6', 'WTDS365-7', 'WTDS365-8', 'WTDS365-9', 'WTDS139-ABR 2', 'WTDS379-3', 'WTDS316-8A1 2', 'WTDS213-ABRC1', 'WTDS55-1', 'WTDS379-14', 'WTDS379-13', 'WTDS379-12', 'WTDS379-11', 'WTDS379-10', 'WTDS55-2', 'WTDS380-3', 'WTDS380-2', 'WTDS353-3C1', 'WTDS273-R-08', 'WTDS380-6', 'WTDS380-5', 'WTDS380-4', 'WTDS273-R-04', 'WTDS273-R-05', 'WTDS273-R-06', 'WTDS273-R-07', 'WTDS234-R-01', 'WTDS234-R-00', 'WTDS273-R-02', 'WTDS273-R-03', 'WTDS427-1', 'WTDS70-ABR', 'WTDS427-3', 'WTDS427-2', 'WTDS427-5', 'WTDS427-4', 'WTDS427-7', 'WTDS427-6', 'WTDS296-6', 'WTDS340-5', 'WTDS379-12A6', 'WTDS342-RA1-00', 'WTDS336-ABR', 'WTDS265-27', 'WTDS265-20', 'WTDS265-21', 'WTDS342-R-01 2', 'WTDS342-R-01 3', 'WTDS46-13', 'WTDS379-12A7', 'WTDS46-7', 'WTDS64-R-01', 'WTDS412-5', 'WTDS64-R-03', 'WTDS64-R-02', 'WTDS336-ABRC1', 'WTDS316-8', 'WTDS103-6', 'WTDS103-7', 'WTDS103-4', 'WTDS103-5', 'WTDS103-2', 'WTDS103-3', 'WTDS103-1', 'WTDS412-R 2', 'WTDS283-16A1 3', 'WTDS283-16A1 2', 'WTDS342-ABR-3', 'WTDS342-ABR-2', 'WTDS103-8', 'WTDS103-9', 'WTDS194-R-02', 'WTDS194-R-00', 'WTDS194-R-01', 'WTDS357-12C1', 'WTDS267-ABR', 'WTDS280-2', 'WTDS342-RA1-01 2', 'WTDS108-5', 'WTDS108-4', 'WTDS108-7', 'WTDS108-6', 'WTDS108-1', 'WTDS108-3', 'WTDS108-2', 'WTDS342-13 3', 'WTDS70-1', 'WTDS70-2', 'WTDS46-2', 'WTDS108-9', 'WTDS108-8', 'WTDS70-6', 'WTDS70-7', 'WTDS46-4', 'WTDS388-9', 'WTDS316-9', 'WTDS234-ABR 2', 'WTDS388-2', 'WTDS388-1', 'WTDS345-R-02', 'WTDS273-6', 'WTDS345-R-00', 'WTDS345-R-01', 'WTDS412-13 2', 'WTDS54-17', 'WTDS295-ABR', 'WTDS138-ABR', 'WTDS273-1', 'WTDS283-5 2', 'WTDS283-5 3', 'WTDS103-R', 'WTDS273-2', 'WTDS273-3', 'WTDS103-ABR', 'WTDS234-14C1', 'WTDS277-R-00', 'WTDS277-R-01', 'WTDS277-R-02', 'WTDS277-R-03', 'WTDS234-R-01 2', 'WTDS317-5A1 2', 'WTDS54-9 2', 'WTDS273-8', 'WTDS379-ABR', 'WTDS342-11', 'WTDS131-1', 'WTDS342-13', 'WTDS342-12', 'WTDS342-15', 'WTDS342-14', 'WTDS412-17A1 2', 'WTDS412-RA1_2', 'WTDS139-4 2', 'WTDS426-4', 'WTDS426-5', 'WTDS426-6', 'WTDS126-R', 'WTDS426-1', 'WTDS426-2', 'WTDS426-3', 'WTDS316-10', 'WTDS267-RA1-05', 'WTDS316-12', 'WTDS316-13', 'WTDS266-36', 'WTDS142-12', 'WTDS316-16', 'WTDS147-1', 'WTDS316-6A1 2', 'WTDS387-5', 'WTDS387-6', 'WTDS387-7', 'WTDS387-1', 'WTDS387-2', 'WTDS387-3', 'WTDS296-R-02', 'WTDS316-6A1', 'WTDS387-9', 'WTDS388-4', 'WTDS126-1', 'WTDS126-3', 'WTDS126-2', 'WTDS126-5', 'WTDS126-4', 'WTDS126-7', 'WTDS126-6', 'WTDS54-RC3', 'WTDS46-R', 'WTDS54-RC1', 'WTDS387-10', 'WTDS54-RC4', 'WTDS295-R-04', 'WTDS46-1', 'WTDS283-13 2', 'WTDS283-13 3', 'WTDS295-R-00', 'WTDS295-R-01', 'WTDS295-R-02', 'WTDS129-1', 'WTDS234-14 2', 'WTDS97-1', 'WTDS317-5A1C1', 'WTDS55-12', 'WTDS218-1', 'WTDS54-15 3', 'WTDS139-7 2', 'WTDS218-2', 'WTDS342-11 2', 'WTDS342-11 3', 'WTDS283-3 2', 'WTDS283-3 3', 'WTDS345-10', 'WTDS194-RC2', 'WTDS345-12', 'WTDS345-13', 'WTDS345-14', 'WTDS345-15', 'WTDS213-8', 'WTDS213-9', 'WTDS236-1', 'WTDS213-7', 'WTDS236-3', 'WTDS236-2', 'WTDS236-5', 'WTDS236-4', 'WTDS213-1', 'WTDS64-3', 'WTDS104-1', 'WTDS104-3', 'WTDS104-2', 'WTDS64-1', 'WTDS104-4', 'WTDS380-1-add.2', 'WTDS380-1-add.3', 'WTDS283-15', 'WTDS283-14', 'WTDS283-17', 'WTDS283-16', 'WTDS283-11', 'WTDS283-10', 'WTDS283-13', 'WTDS283-12', 'WTDS217-2', 'WTDS217-3', 'WTDS217-1', 'WTDS71-1', 'WTDS142-R', 'WTDS217-4', 'WTDS217-5', 'WTDS64-2', 'WTDS387-11', 'WTDS267-RA2-04', 'WTDS267-RA2-05', 'WTDS267-RA2-06', 'WTDS267-RA2-00', 'WTDS267-RA2-01', 'WTDS267-RA2-02', 'WTDS267-RA2-03', 'WTDS296-R-05', 'WTDS46-ABR', 'WTDS342-R-01', 'WTDS342-R-00', 'WTDS142-2', 'WTDS142-1', 'WTDS365-12', 'WTDS365-13', 'WTDS365-10', 'WTDS365-11', 'WTDS412-4', 'WTDS103-10C1', 'WTDS234-14C1 2', 'WTDS353-3', 'WTDS299-9', 'WTDS213-R', 'WTDS353-1', 'WTDS342-RA1-01', 'WTDS341-4', 'WTDS412-10 2', 'WTDS295-14', 'WTDS295-15', 'WTDS295-12', 'WTDS295-13', 'WTDS295-10', 'WTDS295-11', 'WTDS46-8']
reload(sys) 
sys.setdefaultencoding('utf8')

current_file_path = __file__
foldername = os.path.dirname(os.path.realpath(__file__))
stemmer = PorterStemmer()

class back_to_keywords():
	def main(self):
		#newlist = self.read_dict(foldername)
		newlist = ['regard wtoinconsist','inconsist fair','concept fair', 'proceed inconsist', 'norm gener',
					'stare decisi', 'rule norm', 'creat legitim', 'basi oblig', 'held inconsist', 'requir fair',
					'impos unreason', 'read oblig', 'evenhand', 'expect wto','legal rule', 'investig violat',
					'order inconsist', 'unbias object','appli inconsist', 'interpret legal', 'result inconsist',
					'central element', 'disput inconsist', 'bodi jurisprud', 'function wto', 'practic inconsist',
					'wtoinconsist measur', 'violat relev', 'textual basi', 'materi injur', 'interpret relev',
					'inconsist certain','textual analysi', 'interpret public','legal question','establish oblig']
		terminate = False
		key_input_str = input("Please input the dictionary terms you want to search (if you want to input many keywords, please use comma to seperate them. Remember to include quotation mark for all words you input): ")
		key_input = key_input_str.split(',')
		while not terminate:
			count = 0
			if len(key_input) == 1:
				if key_input[0] in newlist:
					terminate = True
				else:
					key_input_str = input("Please input your keywords again: ")
					key_input = key_input_str.split(',')
			elif len(key_input) == 0:
				key_input_str = input("Please input your keywords again: ")
				key_input = key_input_str.split(',')
			else:
				for word in key_input:
					if word not in newlist:
						key_input_str = input("Please input your keywords again: ")
						key_input = key_input_str.split(',')
						count = 0
						break
						#continue
					else:
						count += 1
			if count == len(key_input):
				terminate = True
		set_B, set_B_name = self.convert_B_to_list(foldername)
		for word in key_input:
			check = mapping[word]
			index_list = []
			for check_words in check:
				if check_words.count(' ') == 0:
					for doc_name in set_name:
						if check_words in set_B[doc_name]:
							index_list=[n for n in xrange(len(set_B[doc_name])) if set_B[doc_name].find(check_words, n) == n]
							for index in index_list:
								print doc_name
								print
								print set_B[doc_name][index - 100:index] + color.BLUE + color.BOLD + set_B[doc_name][index: index + 11] + color.end + set_B[doc_name][index+11:index + 110]
								print 
				elif check_words.count(' ') == 1:
					#check_words = check_words.split()
				 	for doc_name in set_name:
				 		if check_words in set_B[doc_name]:
				 			index_list1 = [n for n in xrange(len(set_B[doc_name])) if set_B[doc_name].find(check_words, n) == n]
				 			for index in index_list1:
				 				print doc_name
				 				print 
				 				print set_B[doc_name][index - 100:index] + color.BLUE + color.BOLD + set_B[doc_name][index:index+20] + color.end + set_B[doc_name][index+21:index + 110]
				 				print
				 		else:
				 			check_words_list = check_words.split()
					 	 	if check_words_list[0] in set_B[doc_name] and check_words_list[1] in set_B[doc_name]:
					 	 		index_list1 = [n for n in xrange(len(set_B[doc_name])) if set_B[doc_name].find(check_words_list[0], n) == n] + [n for n in xrange(len(set_B[doc_name])) if set_B[doc_name].find(check_words_list[1], n) == n]
					 	 		print index_list1
					 	 		for index in index_list1:
					 	 			print doc_name
					 	 			print
					 	 			print set_B[doc_name][index - 100:index] + color.BLUE + color.BOLD + set_B[doc_name][index:index+10] + color.end + set_B[doc_name][index+11:index + 110]
					 	 			print 
			#if check_words.count(' ') == 1:

			#if check_words.count(' ') == 2:

		# cv = CountVectorizer(vocabulary=key_input,ngram_range=(1, 2),stop_words = 'english',decode_error='ignore',tokenizer = self.tokenize)
		# set_B_case, set_B_name_dict = self.convert_B_to_list(foldername)
		# new_matrix = cv.fit_transform(set_B_case)
		# nonzero = np.nonzero(new_matrix)

	# def stem_original_dict(self):
	# 	stem_term = self.read_dict(foldername)
	# 	stem_term_dict = dict(enumerate(stem_term))
	# 	##sample dict
	# 	stem_term_dict_final = {}
	# 	for i in xrange(0,37):
	# 		stem_term_dict_final[i] = stem_term_dict[i]
	# 	#stem_term_dict = stem_term_dict[1]
	# 	stem_term_dict_final = {y:x for x,y in stem_term_dict_final.iteritems()}

	# 	cv1 = CountVectorizer(ngram_range=(1, 2),stop_words = 'english',decode_error='ignore')
	# 	##each document is a list
	# 	sample_text = self.convert_A_to_list(foldername)
	# 	a1 = cv1.fit_transform(sample_text)
	# 	blist = cv1.get_feature_names()
	# 	blist_final = [x.encode('UTF8') for x in blist]
	# 	# cvv = CountVectorizer(ngram_range=(1, 2),stop_words = 'english', decode_error='ignore',tokenizer = self.tokenize)
	# 	# c = cvv.fit_transform(sample_text)
	# 	# single_token_list =  cvv.get_feature_names()
	# 	# single_token =  [y.encode('UTF8') for y in single_token_list]
	# 	# print len(single_token)
	# 	# map_dict = dict(zip(single_token, blist_final))
	# 	# print map_dict[:10]
	# 	# for item in map_dict:
	# 	# 	if item in stem_term_dict_final:
	# 	# 		stem_term_dict_final[item] = map_dict[item]
	# 	for j in blist_final:
	# 		try:
	# 			#print j
	# 			#cvv = CountVectorizer(ngram_range=(1, 2),stop_words = 'english', decode_error='ignore',tokenizer = self.tokenize)
	# 			#c = cvv.fit_transform([j])
	# 			#print cvv.get_feature_names()[0]
	# 			#single_token_list =  cvv.get_feature_names()
	# 			#single_token = [y.encode('UTF8') for y in single_token_list]
	# 			#print single_token
	# 			#for item in single_token:
	# 			item = stemmer.stem(j)
	# 			#print item
	# 			if item in stem_term_dict_final:
	# 				if type(stem_term_dict_final[item]) == int:
	# 					stem_term_dict_final[item] = [j]
	# 				else:
	# 					if stem_term_dict_final[item] != [j]:
	# 						stem_term_dict_final[item] += [j]
	# 		except:
	# 			continue
	# 	print stem_term_dict_final
	# 	return stem_term_dict_final

	def read_dict(self,foldername):
		data_dir = os.path.join(foldername, 'dictionary_terms.xlsx')
		data = get_data(data_dir)
		jsondata = json.dumps(data)
		jsondata = jsondata[105:-3]
		data_list = jsondata.split('],')
		newlist = []
		for line in data_list:
			line = line.split(',')[0].replace('"','').replace('[','').strip()
			newlist.append(line)
		return newlist


	def convert_A_to_list(self, foldername):
		data_dir = os.path.join(foldername, 'SET_B_subsidies')
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
		set_B = {}
		for filename in os.listdir(data_dir):
			if filename != '.DS_Store':
				newFilename = filename[:-4]
				item = ''
				f = open(data_dir+'/'+filename,'r')
				item = f.read()
				f.close()
				item = item.replace('/n','')
				set_B[newFilename] = item
				#print set_B
				#break
		#set_B_doc = set_B.values()
		set_B_name = set_B.keys()
		#set_B_name_dict = dict(enumerate(set_B_name))
		#print set_B_name
		return set_B, set_B_name

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
					###record how many documents in a case
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

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   end = "\033[0;0m"

o = back_to_keywords()
#o.convert_B_to_list(foldername)
#o.read_dict(foldername)
o.main()
