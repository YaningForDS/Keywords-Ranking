import os
import csv
import numpy as np
current_file_path = __file__
foldername = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(foldername, 'sheet2_B_bigram.csv')
filename = open(data_dir,'r')
newfile = open('sheet3_B_bigram.csv','w')
fieldnames = ['Stemmed Term','mean case doc freq over all B cases','median case doc freq over all B cases','SD of case doc freq over all B cases']
writer = csv.DictWriter(newfile,fieldnames=fieldnames)
writer.writeheader()

filename.readline()
for line in filename:
	new_dict = {}
	newline = line.split(',')
	new_dict = {'Stemmed Term': newline[0]}
	numerical = []
	for element in newline[1:]:
		element = float(element)
		numerical.append(element)
	newmean = np.mean(numerical)
	newmedian = np.median(numerical)
	newstd = np.std(numerical)
	new_dict['mean case doc freq over all B cases'] = newmean
	new_dict['median case doc freq over all B cases'] = newmedian
	new_dict['SD of case doc freq over all B cases'] = newstd
	writer.writerow(new_dict)


