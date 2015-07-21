__author__ = 'HongDing'

from monty.serialization import loadfn, dumpfn
import os
import glob
import nltk

Dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'50','cleaned')

for stemmer_fld in glob.glob(os.path.join(Dir,'*')):

    Comparison = []

    stemmer = stemmer_fld.split('/')[-1]

    for fld in glob.glob(os.path.join(stemmer_fld,'*')):
        if os.path.isdir(fld):

            hint = [loadfn(os.path.join(fld,str(i)+'.json')) for i in range(2)]

            all_words = set(word.lower() for passage in hint for word in passage.keys())

            t = [({word: (word in hint[i]) for word in all_words}, i) for i in range (2)]



            classifier = nltk.NaiveBayesClassifier.train(t)

            test_features = loadfn(os.path.join(fld,'paragraph.json'))

            if os.path.exists(os.path.join(fld, 'Answer_0')):
                Comparison.append((0,classifier.classify(test_features)))
            elif os.path.exists(os.path.join(fld, 'Answer_1')):
                Comparison.append((1,classifier.classify(test_features)))
            else:
                Comparison.append((-1,classifier.classify(test_features)))

    print ' %s : Correct ratio is %.2f' % \
          (stemmer,(float(len(filter(lambda entry:entry[0]==entry[1],Comparison)))/len(Comparison)))



