import matplotlib.pyplot as plt
from collections import OrderedDict
# myDictionary = { 'WTDS46': 0.23839137645107794,'WTDS51': 0.66225165562913912, 'WTDS52': 0.37383177570093457,
# 'WTDS54': 0.30244707176244157, 'WTDS55': 0.71599045346062051, 'WTDS57': 1.6666666666666667, 
# 'WTDS59': 0.82063305978898005,'WTDS64': 0.14579857117400249, 'WTDS65': 0.92307692307692313,'WTDS71': 0.0, 
# 'WTDS70': 0.15353552349303831,'WTDS81': 0.25062656641604009, 'WTDS97': 0.80000000000000004,
# 'WTDS104': 0.36231884057971014, 'WTDS106': 1.5151515151515151,'WTDS108': 0.35842293906810035, 
# 'WTDS112': 0.77519379844961245, 'WTDS126': 0.23634453781512604, 'WTDS127': 0.625, 'WTDS128': 0.7142857142857143, 
# 'WTDS129': 0.69444444444444442,'WTDS130': 0.64516129032258063, 'WTDS131': 0.49751243781094528,
# 'WTDS138': 0.15254865212369517, 'WTDS139': 0.35780240073868885, 'WTDS142': 0.14593090341410439, 'WTDS145': 0.0, 'WTDS147': 0.0,
# 'WTDS167': 0.43103448275862066, 'WTDS172': 0.0, 'WTDS173': 0.0,'WTDS194': 0.27891767119774302, 'WTDS195': 0.39564787339268054,
# 'WTDS206': 0.19562367651507512,'WTDS212': 0.21585839689163908, 'WTDS213': 0.25403168260311115, 'WTDS217': 0.38022813688212925,
# 'WTDS218': 0.75046904315196994, 'WTDS221': 0.42190222874438227, 'WTDS222': 0.1323647594585651,
# 'WTDS234': 0.1923570146191331,'WTDS236': 0.24231362306070428, 'WTDS257': 0.18674136321195145,'WTDS262': 0.18248175182481752, 
# 'WTDS265': 0.23296915167095117,'WTDS266': 0.23326272890581012, 'WTDS267': 0.056657223796033995, 
# 'WTDS273': 0.10225762103325645, 'WTDS277': 0.21757322175732219,'WTDS280': 0.84269662921348309,'WTDS283': 0.17244382511757533,
# 'WTDS295': 0.18696111208868554,'WTDS296': 0.13835131351395866,'WTDS299': 0.18953752843062927, 'WTDS301': 0.26504108136761195,
# 'WTDS307': 0.17636684303350969,'WTDS310': 1.5317286652078774,'WTDS330': 0.98039215686274506,
# 'WTDS311': 0.084332833583208394, 'WTDS314': 1.408450704225352, 'WTDS316': 0.051695570529106373,
# 'WTDS317': 0.076359193646915083,'WTDS336': 0.19154903883428728, 'WTDS339': 0.38610038610038611,'WTDS340': 0.25062656641604009,
# 'WTDS341': 0.25072653712462251,'WTDS342': 0.11378739924077988, 'WTDS345': 0.22910132278739942,'WTDS347': 0.0,
# 'WTDS353': 0.060955649121222727,'WTDS354': 0.39370078740157483, 'WTDS357': 0.10961907371882708,
# 'WTDS357': 0.10961907371882708,'WTDS358': 0.2058672156459084,'WTDS359': 0.39840637450199201,'WTDS365': 0.034002040122407345,
# 'WTDS368': 1.2244897959183674, 'WTDS379': 0.13935340022296544,'WTDS380': 0.28228652081863093,'WTDS385': 1.2121212121212122, 
# 'WTDS387': 0.039385584875935409, 'WTDS388': 0.1168679392286716,'WTDS390': 0.041511000415110001,'WTDS412': 0.14783963373922995,
# 'WTDS414': 0.17149753339967394,'WTDS419': 0.64516129032258063, 'WTDS426': 0.49176297024834031, 'WTDS427': 0.17413136794363004
# }

myDictionary = {'WTDS167': 0.0, 'WTDS283': 0.017418568193694479, 'WTDS280': 0.0, 'WTDS368': 0.0, 'WTDS206': 0.032267822930321668, 'WTDS51': 0.0, 'WTDS57': 0.0, 'WTDS55': 0.0, 'WTDS54': 0.0, 'WTDS59': 0.0, 'WTDS365': 0.0, 'WTDS354': 0.0, 'WTDS357': 0.0, 'WTDS299': 0.021322971948445794, 'WTDS353': 0.0079016582194177606, 'WTDS295': 0.024194967446771073, 'WTDS296': 0.01976447335913695, 'WTDS359': 0.0, 'WTDS112': 0.0, 'WTDS195': 0.0, 'WTDS194': 0.025647601949217749, 'WTDS212': 0.03237875953374586, 'WTDS213': 0.025688597117168546, 'WTDS218': 0.0, 'WTDS358': 0.0, 'WTDS342': 0.015299146116407378, 'WTDS340': 0.0, 'WTDS341': 0.022793321556783864, 'WTDS108': 0.0, 'WTDS347': 0.0, 'WTDS419': 0.0, 'WTDS104': 0.0, 'WTDS106': 0.0, 'WTDS412': 0.01271738784853591, 'WTDS221': 0.03668715032559846, 'WTDS222': 0.017333480405288287, 'WTDS139': 0.0, 'WTDS138': 0.019613398130189377, 'WTDS131': 0.0, 'WTDS130': 0.0, 'WTDS336': 0.011401728502040909, 'WTDS330': 0.0, 'WTDS236': 0.018881581017717218, 'WTDS81': 0.0, 'WTDS234': 0.03114351665262155, 'WTDS339': 0.0, 'WTDS64': 0.016199841241555834, 'WTDS65': 0.0, 'WTDS126': 0.013130252100840336, 'WTDS127': 0.0, 'WTDS128': 0.0, 'WTDS129': 0.0, 'WTDS97': 0.0, 'WTDS52': 0.0, 'WTDS217': 0.0, 'WTDS426': 0.0, 'WTDS71': 0.0, 'WTDS70': 0.0042064526984394064, 'WTDS390': 0.0, 'WTDS311': 0.0, 'WTDS310': 0.21881838074398249, 'WTDS314': 0.352112676056338, 'WTDS317': 0.0, 'WTDS316': 0.0075113222136308404, 'WTDS257': 0.017507002801120448, 'WTDS387': 0.0, 'WTDS142': 0.011878096789520124, 'WTDS385': 0.0, 'WTDS145': 0.0, 'WTDS380': 0.0, 'WTDS147': 0.0, 'WTDS388': 0.0, 'WTDS265': 0.021422450728363324, 'WTDS267': 0.010540878845773767, 'WTDS266': 0.021449446336166449, 'WTDS262': 0.0, 'WTDS46': 0.010364842454394693, 'WTDS307': 0.044091710758377423, 'WTDS301': 0.015145204649577828, 'WTDS173': 0.0, 'WTDS172': 0.0, 'WTDS427': 0.018223050133635701, 'WTDS273': 0.010225762103325644, 'WTDS277': 0.019525801952580194, 'WTDS345': 0.027273966998499932, 'WTDS379': 0.015752993068683049, 'WTDS414': 0.010586267493807033}

key = myDictionary.keys()
x = []
w_freq = []
for elem in key:
	elem = int(elem[4:])
	x.append(elem)
x_sorted = sorted(x)
for i in x_sorted:
	w_freq.append(myDictionary['WTDS'+str(i)])
print x_sorted
print w_freq
x = []
for j in x_sorted:
	x.append('WTDS'+str(j))

plt.bar(range(len(w_freq)), w_freq)
plt.xticks(range(len(w_freq)), x, fontsize = 5,rotation=90)

plt.show()

sorted_x = OrderedDict(sorted(myDictionary.items(), key=lambda t: t[1]))
index = sorted_x.values()
keys = sorted_x.keys()
print index
print keys
index_re = index[::-1]
keys_re = keys[::-1]

print index_re
print keys_re
plt.bar(range(len(index_re)), index_re)
plt.xticks(range(len(index_re)), keys_re, fontsize = 5,rotation=90)

plt.show()




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

print color.BLUE + color.BOLD +'Hello World !' + color.end