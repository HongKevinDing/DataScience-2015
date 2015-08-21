# -*- coding: utf-8 -*-

## CDIPS 2015 Workshop Project
## Team: Acronyms
## Members: Hong Ding, Philipp Dumitrescu, Herman Leung
## July 11 - Aug 1, 2015

## This file is an early test on the acronym_extract.py file

'''
This file takes as input a directory of folders, each of which belongs to an
acronym with two possible meanings. Each of these folders contain the following
items:

    (1) 0.txt - text from a Wikipedia page of acronym with meaning #1
    (2) 1.txt - text from a WIkipedia page of same acronym but with meaning #2
    (3) paragraph - text randomly taken from the internet containing
                    the acronym matching meaning #1 or #2
    (4) Answer_1 or Answer_0 - indicates which file 'paragraph' matches
                               in terms of the acronym meaning

This file uses functions in acronym_extract.py to extract acronyms from the
0.txt and 1.txt files and checks if it extracted the acronym represented by
the folder containing those files. Some basic numbers and lists are created
in print and as .txt files.
'''

import nltk, re, os, sys
from nltk import word_tokenize
from nltk.corpus import stopwords

from acronym_extract import extract_acronym as EA


# Input directory (with subfolders of files)
DIR = '/Users/herman/Documents/CDIPS-DSW-2015/DataScience-2015/Acronym_Workspace/Testing/50/raw/'

# Output directory
DIR2 = '/Users/herman/Documents/CDIPS-DSW-2015/DataScience-2015_self/'

folders = [name for name in os.listdir(DIR) \
           if os.path.isdir(os.path.join(DIR, name))]

accuracy_list = []
grand_list = []
acronyms_detected = []

for folder in folders:
    for number in ['0', '1']:
        with open(DIR + folder + '/' + number + '.txt', 'r') as f:
            text = f.read()
            EAlist = EA(text, search='simple')
            grand_list += [EAlist]
            if EAlist not in [None, []]:
                acronyms_detected += [(folder + '-' + number, len(EAlist))]
                if folder in [item[0] for item in EAlist]:
                    accuracy_list += [(folder, 1)]
                else:
                    accuracy_list += [(folder, 0)]
            else:
                acronyms_detected += [(folder + '-' + number, 0)]
                accuracy_list += [(folder, 0)]


accuracy_rate = sum([item[1] for item in accuracy_list])/float(len(accuracy_list))
print('The accuracy rate of the acronym extractor on our 100 (50*2) samples: ' + str(accuracy_rate))

sum_acronyms_detected = sum([item[1] for item in acronyms_detected])
print('Number of acronyms detected on our 100 (50*2) samples: ' + str(sum_acronyms_detected))

with open(DIR2 + 'EA_accuracy_list.txt', 'w') as f:
    for a in accuracy_list:
        f.write(str(a) + '\n')

with open(DIR2 + 'EA_grand_list.txt', 'w') as f:
    for g in grand_list:
        if len(g) > 1:
            f.write(str(g[0]) + '\n')
            for sublist in g[1:]:
                f.write('\t' + str(sublist) + '\n')
        else:
            f.write(str(g) + '\n')

with open(DIR2 + 'EA_acronyms_detected.txt', 'w') as f:
    for a in acronyms_detected:
        f.write(str(a) + '\n')
