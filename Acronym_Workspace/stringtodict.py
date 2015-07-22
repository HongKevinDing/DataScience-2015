# -*- coding: utf-8 -*-

### CDIPS 2015 Project
### Team: Kevin Ding, Philipp Dumitrescu, Herman Leung
### Acronym Detection/Disambiguation
'''
'''

import nltk, re, json, sys
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
wordnet = WordNetLemmatizer()

class StringToDict():
    def __init__(self, text, stemmer='unstemmed', delete_stopwords=True):
        self._text = text
        self._lower = self._text.lower()
        self._clean = re.sub('\s', ' ', self._lower)
        self._clean2 = re.sub('[^\w ]', '', self._clean)
        self._list = self._clean2.split(' ')
        if delete_stopwords:
            self.cleanlist = [word for word in self._list if (word != '' \
                           and word not in stopwords.words('english') )]
        else: 
            self.cleanlist = [word for word in self._list if (word != '')]

        # Stemming options, default unstemmed
        if stemmer == 'unstemmed':
            self.fqdist = FreqDist(self.cleanlist)
        elif stemmer == 'porter':
            porter_list = [porter.stem(word) for word in self.cleanlist]
            self.fqdist = FreqDist(porter_list)
        elif stemmer == 'lancaster':
            lancaster_list = [lancaster.stem(word) for word in self.cleanlist]
            self.fqdist = FreqDist(lancaster_list)
        elif stemmer == 'wordnet':
            wordnet_list = [wordnet.lemmatize(word) for word in self.cleanlist]
            self.fqdist = FreqDist(wordnet_list)
        else:
            print('Choose between "unstemmed", "porter", "lancaster", "wordnet"')

    def counts_dict(self):
        counts = dict(self.fqdist)
        return counts

    def freq_dict(self):
        cleanlist2 = [word for word in self._list if word != '']
        text_count = len(cleanlist2)
        fqdict = dict(self.fqdist)
        frequencies = [(k,(float(v)/text_count)) for (k,v) in fqdict.items()]
        frequencies = dict(frequencies)
        return frequencies

text = '''
United Carolina Bank
From Wikipedia, the free encyclopedia
United Carolina Bank (UCB) was a bank headquartered in Whiteville, North Carolina. It was formed in 1980 by the merger of four banks, including Waccamaw Bank of Whiteville. BB&T took over UCB in 1997.
History[edit]
In 1926, business people in Whiteville raised $10,000 and started Waccamaw Bank and Trust, named for an area lake and river.[1]
American Bank & Trust of Monroe, North Carolina began May 5, 1930 in the Monroe Hotel after the failure of Bank of Union during The Great Depression. In 1970 it merged with Waccamaw Bank and Trust to form United Carolina Bancshares, though it kept the American name until 1979. UCB also took over Cape Fear Bank of Fayetteville, North Carolina and Capital National Bank of Raleigh, North Carolina.[2][3][4]
In 1981, UCB opened an 83,000-square-foot (7,700 m2) operations center near Monroe, which employed 250 people.[5]
In 1982, UCB bought the Bank of Raeford.[6]
When E. Rhone Sasser became chief executive in 1983, UCB had $857 million in assets.[7]
In 1986, UCB took over Bank of Greer with $150 million in assets and eight offices in Greenville and Spartanburg Counties, for $284 million. The Bank of Greer offices began operating as United Carolina Bank of South Carolina.[8]
In 1987, UCB began opening branches in Winn-Dixies in North Carolina, joining Central Carolina Bank and Trust as the second bank in the state to open grocery store branches in North Carolina.[9] The first branch was not a success, however, and the plan was dropped.[10]
Also in 1987, UCB announced a new four-story building to house 200 workers next to its headquarters in Whiteville, putting an end to rumors the bank would move its headquarters to Charlotte, where the Johnston Building was called the UCB Building. At the time, UCB had $1.9 billion in assets and 114 locations. 380 of its employees worked in Whiteville, a town of 5565 people.[11][12]
In 1991, UCB added its second and third branches in Moore County. The bank had an Aberdeen branch already when it opened a Pinehurst location. Also, UCB was buying a Barclays Bank branch in Southern Pines.[13]
In 1994, UCB bought its first western North Carolina bank, Bank of Iredell in Statesville, with 79.4 million in assets and five branches.[14]
In October 1995, UCB agreed to buy Triad Bank, the last locally owned bank in Greensboro in a deal valued at $40 million. When the deal was completed, UCB would have branches in the Piedmont Triad for the first time. Triad Bank had eleven branches, eight of those in Greensboro, and assets of $199 million, and had taken over Bankers Trust of North Carolina in 1993; Bankers Trust had in turn taken over Piedmont State Bank.[15]
UCB's fourth acquisition of the 1990s was Seaboard Savings Bank of Plymouth, North Carolina. UCB was North Carolina's eighth-largest bank with assets of $3.7 billion. However, other banks in the state were doing a better job of growing through mergers.[1]
In 1997, Southern National Corp. of Winston-Salem, North Carolina, which operated as BB&T, took over UCB in a $985 million deal announced in November 1996. UCB had $4.5 billion in assets. 400 employees worked in Whiteville but despite losing the headquarters, the town would eventually have 500 BB&T employees working at a 250-employee call center and other operations.[3][5] Starting September 22, 1997, 91 UCB branches began the process of changing to BB&T, and 67 other branches of the two banks closed starting in October because they were close to other BB&T locations.[16][17] South Piedmont Community College bought the Monroe operations center in 2000 to serve as its Monroe Continuing Education Center, later expanding the campus at the site.[18]
'''

cleanlist = StringToDict(text, 'unstemmed')
counts = cleanlist.counts_dict()
freqs = cleanlist.freq_dict()

############################################
### Create json file of count dictionary ###
############################################
#print counts
f_json = open('UCBank2.json','w')
json.dump(counts,f_json,indent=4)
f_json.close()
############################################

###############################################
### Test functions in dictionary_stemmer.py ###
###############################################
# import dictionary_stemmer as ds
#
# porter_dict = ds.stem_dict(counts, 'porter')
# lancaster_dict = ds.stem_dict(counts, 'lancaster')
# wordnet_dict = ds.stem_dict(counts, 'wordnet')
#
# print('Length of unstemmed dict: ' + str(len(counts)))
# print('Length of Porter-stemmed dict: ' + str(len(porter_dict)))
# print('Length of Lancaster-stemmed dict: ' + str(len(lancaster_dict)))
# print('Length of Wordnet-lemmatized dict: ' + str(len(wordnet_dict)))
#
# if sum(counts.values()) == sum(porter_dict.values()) == \
#         sum(lancaster_dict.values()) == sum(wordnet_dict.values()):
#     print('Dictionary_stemmer.py seems to be working correctly.')
###############################################

#stopwords = stopwords.words('english')
#print(len(stopwords))
#print(stopwords)
