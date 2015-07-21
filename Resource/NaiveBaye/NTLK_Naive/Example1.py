__author__ = 'HongDing'

train = [('I love this sandwich.', 'pos'),
('This is an amazing place!', 'pos'),
('I feel very good about these beers.', 'pos'),
('This is my best work.', 'pos'),
("What an awesome view", 'pos'),
('I do not like this restaurant', 'neg'),
('I am tired of this stuff.', 'neg'),
("I can't deal with this", 'neg'),
('He is my sworn enemy!', 'neg'),
('My boss is horrible.', 'neg')]

from nltk.tokenize import word_tokenize # or use some other tokenizer
all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]

print t

import nltk
classifier = nltk.NaiveBayesClassifier.train(t)
classifier.show_most_informative_features()

test_sentence = "This is the best band I've ever heard!"
test_sent_features = {word.lower(): (word in word_tokenize(test_sentence.lower())) for word in all_words}

print classifier.classify(test_sent_features)
