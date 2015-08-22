# -*- coding: utf-8 -*-

### CDIPS 2015 Project
### Team: Acronyms
### Members: Hong Ding, Philipp Dumitrescu, Herman Leung
### July 11 - Aug 1, 2015

'''
This file takes text files in Acronym_Workspace/Testing/50/raw/ and stems/lemmatizes them.
The output is in Acronym_Workspace/Testing/50/cleaned/ and include subfolders according
to different stemming/lemmatizing methods.
'''

import re, json, os, shutil
import stringtodict as std

DIR = '/Users/herman/Documents/CDIPS-DSW-2015/DataScience-2015/Acronym_Workspace/Testing/50/'
rawDIR = DIR + 'raw2_fix/'        # Input directory
cleanDIR = DIR + 'cleaned2_fix/'  # Output directory

unstemmedDIR = cleanDIR + 'unstemmed/'
porterDIR = cleanDIR + 'porter/'
lancasterDIR = cleanDIR + 'lancaster/'
wordnetDIR = cleanDIR + 'wordnet/'

cleanSUBDIR_list = [unstemmedDIR, porterDIR, lancasterDIR, wordnetDIR]
stem_type = ['unstemmed', 'porter', 'lancaster', 'wordnet']


def process_to_files(inputDIR, outputLIST, stemtypeLIST):
    assert (len(outputLIST) == len(stemtypeLIST)), \
        'outputLIST and stemtypeLIST must have same number of items'

    acronym_list = [name for name in os.listdir(rawDIR) \
                    if os.path.isdir(os.path.join(rawDIR, name))]

    outLIST = zip(outputLIST, stemtypeLIST)
    for (outDIR, stemtype) in outLIST:
        for acronym in acronym_list:
            acroDIR_old = os.path.join(inputDIR, acronym + '/')
            acroDIR_new = os.path.join(outDIR, acronym + '/')
            if not os.path.exists(acroDIR_new):
                os.mkdir(acroDIR_new)
            answerFile = re.search('A.*?[01]', \
                        str([filename for filename in os.listdir(acroDIR_old)])).group()
            shutil.copyfile(acroDIR_old + answerFile, acroDIR_new + answerFile)
            filesLIST = ['0.txt', '1.txt', 'paragraph']
            for f in filesLIST:
                with open(acroDIR_old + f, 'r') as inputfile:
                    text = inputfile.read()
                cleanlist = std.StringToDict(text, stemtype)
                counts = cleanlist.counts_dict()
                if re.search('txt', f):
                    f = re.sub('txt', 'json', f)
                else:
                    f += '.json'
                with open(acroDIR_new + f, 'w') as outfile:
                    json.dump(counts, outfile, indent=4)

process_to_files(rawDIR, cleanSUBDIR_list, stem_type)
