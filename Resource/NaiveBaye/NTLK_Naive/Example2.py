import numpy as np
from nltk.probability import FreqDist
from nltk.classify import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

pipeline = Pipeline([('tfidf', TfidfTransformer()),
                     ('chi2', SelectKBest(chi2, k=1000)),
                     ('nb', MultinomialNB())])
classif = SklearnClassifier(pipeline)

from nltk.corpus import movie_reviews
pos = [FreqDist(movie_reviews.words(i)) for i in movie_reviews.fileids('pos')]
neg = [FreqDist(movie_reviews.words(i)) for i in movie_reviews.fileids('neg')]

print pos
add_label = lambda lst, lab: [(x, lab) for x in lst]

#print add_label

print add_label(pos[:100], 'pos')

classif.train(add_label(pos[:100], 'pos') + add_label(neg[:100], 'neg'))

l_pos = np.array(classif.classify_many(pos[100:]))
l_neg = np.array(classif.classify_many(neg[100:]))
print "Confusion matrix:\n%d\t%d\n%d\t%d" % (
          (l_pos == 'pos').sum(), (l_pos == 'neg').sum(),
          (l_neg == 'pos').sum(), (l_neg == 'neg').sum())