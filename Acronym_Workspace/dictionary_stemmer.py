# -*- coding: utf-8 -*-

### CDIPS 2015 Project
### Team: Kevin Ding, Philipp Dumitrescu, Herman Leung
### Acronym Detection/Disambiguation
'''
'''

import nltk, re
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
wordnet = WordNetLemmatizer()

def reduce_list(LIST):
    DICT = {}
    for (k,v) in LIST:
        if k in DICT.keys():
            DICT[k] += v
        else:
            DICT[k] = v
    return DICT

def stem_dict(dictionary, stemmer):
    ''' For the stemmer argument, choose 'wordnet', 'porter', or 'lancaster'
        'wordnet' is the least aggressive, 'lancaster' the most aggressive '''
    if stemmer == 'porter':
        porter_list = [(porter.stem(k),v) for (k,v) in dictionary.items()]
        newdict = reduce_list(porter_list)
    elif stemmer == 'lancaster':
        lancaster_list = [(lancaster.stem(k),v) for (k,v) in dictionary.items()]
        newdict = reduce_list(lancaster_list)
    elif stemmer == 'wordnet':
        wordnet_list = [(wordnet.lemmatize(k),v) for (k,v) in dictionary.items()]
        newdict = reduce_list(wordnet_list)
    elif stemmer == 'unstemmed':
        newdict = dictionary
    else:
        print('Choose "porter", "lancaster", or "wordnet" for stemmer argument')
        newdict = dictionary
    return newdict


# Examples:
newDict = {'apple': 3, 'apples': 2, 'orange': 1, 'eat': 5, 'eating': 4, 'eater': 3}
porterDict = stem_dict(newDict, 'porter')
lancasterDict = stem_dict(newDict, 'lancaster')
wordnetDict = stem_dict(newDict, 'wordnet')

print('original: ' + str(newDict))
print('porter: ' + str(porterDict))
print('lancaster: ' + str(lancasterDict))  # most aggressive
print('wordnet: ' + str(wordnetDict))      # least aggressive
