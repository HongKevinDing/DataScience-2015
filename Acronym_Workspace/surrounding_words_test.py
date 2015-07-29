# -*- coding: utf-8 -*-

### CDIPS 2015 Project
### Team: Kevin Ding, Philipp Dumitrescu, Herman Leung
### Acronym Detection/Disambiguation

import json
import os
import glob
import math

def AddCounts(my_dict_cout):
    count = 0
    for value in my_dict_cout.itervalues():
        count += value
    return count

def MapCountToFreq(english_lang_freq, my_englang_totalcount):
    for key, value in english_lang_freq.iteritems():
        english_lang_freq[key] *= 1.0 / (my_englang_totalcount)
    return

# Weighted: Rare words produce less of an impact than common words 
def MetricWighted(paragraph_fre, compare_article_freq, ref_corpus_freq, test_paragraph):
    overlap = 0.0
    for key, value in paragraph_fre.iteritems():
        if(key in compare_article_freq):
            if(key in ref_corpus_freq):
                key_overlap_contrib = abs(compare_article_freq[key] * value) * (1.0 / float(ref_corpus_freq[key]))
            else:
                key_overlap_contrib = abs(compare_article_freq[key] * value) 
            overlap += key_overlap_contrib
            test_paragraph[key] = key_overlap_contrib
        else:
            test_paragraph[key] = 0
    return overlap
    
# No weighting in the one below. Sort according to lowest ones
def LogMetric(paragraph_fre, compare_to_dict_freq):
    metric = 0.0
    for key, value in paragraph_fre.iteritems():
        metric += value  * abs(math.log(compare_to_dict_freq[key] / value))
    return metric 

def MakeCorpusFreq(ref_corpus, corpus_clean, acronym_path):
    # reads in reference corpus and return frequency dictionary
    corpus_dir = os.path.join(acronym_path, "Word_Frequency", corpus_clean)
    corpus_path = glob.glob(corpus_dir + "/" + ref_corpus + "*.json")
    if(len(corpus_path) != 1):
        raise RuntimeError('Reference Corpus Not Found!')
    my_englang_freq = json.load(open(corpus_path[0])) 
    my_englang_totalcount = AddCounts(my_englang_freq)
    MapCountToFreq(my_englang_freq, my_englang_totalcount)
    return my_englang_freq
    
def RunSingleTest(dictionary_clean, corpus_freq, acronym_path, verbose=False):
    test_dir = os.path.join(acronym_path,'Testing','50','cleaned')
    success = 0
    fail   = 0
    clean_dir = os.path.join(test_dir, dictionary_clean)
    subfolder_names =  [name for name in os.listdir(clean_dir) \
                        if os.path.isdir(os.path.join(clean_dir, name))]
    for acronym in subfolder_names:
        acronym_dir = os.path.join(clean_dir, acronym)
        #Load Three Jason Files
        words0 = json.load(open(os.path.join(acronym_dir,'0.json')))
        words1 = json.load(open(os.path.join(acronym_dir,'1.json')))
        wordsP = json.load(open(os.path.join(acronym_dir,'paragraph.json')))
        # Count Total Number of Words
        words0_counts = AddCounts(words0)
        words1_counts = AddCounts(words1)
        wordsP_counts = AddCounts(wordsP)
        # Make Frequency list out of count list
        MapCountToFreq(words0,words0_counts)
        MapCountToFreq(words1,words1_counts)
        MapCountToFreq(wordsP,wordsP_counts)
        # Dictionary to hold contirbutions to weighting
        contrib0 = {}
        contrib1 = {}
        # Do Comparison
        metric0 = MetricWighted(wordsP, words0, corpus_freq, contrib0)
        metric1 = MetricWighted(wordsP, words1, corpus_freq, contrib1)
            
        if(metric0 > metric1):
            guess = '0'
        else:
            guess = '1'
        if os.path.exists(os.path.join(acronym_dir, 'Answer_0')):
            ref_answer = '0'
        elif os.path.exists(os.path.join(acronym_dir, 'Answer_1')):
            ref_answer = '1'
        else:
            print 'FAIL: Could not find answer file.'
        if (guess == ref_answer):
            success +=1
        else:
            fail += 1
            test_ratio = metric0/metric1 if (guess=='0') else metric1/metric0
            if(verbose==True):
                print "%8s : 0: %4.2e, 1: %4.2e, wrongness: %6.2f" % (acronym, metric0, metric1, test_ratio)
    if (verbose==True):
        print "Correct: " + str(success)
        print "Failed : " + str(fail)
        print "Success: " + str(success / (float(success + fail))) 
    return

def main():
    # runs test cases
    verbose = True
    acronym_path =  os.path.dirname(__file__)
    list_of_cleans = ["unstemmed", "porter", "lancaster", "wordnet", "allwords"]
    corpus = ["ANC_count" ,"Beautiful_Data"]
    list_of_cleans_corpus = ["allwords", "porter", "lancaster"]
    for ref_corpus in corpus:
        for corpus_cleaner in list_of_cleans_corpus:
            corpus_freq = MakeCorpusFreq(ref_corpus, corpus_cleaner, acronym_path)
            for word_cleaner in list_of_cleans:
                if(verbose==True):
                    print "====="
                    print "English Language Corpus: " + ref_corpus + " (" + corpus_cleaner + ")"
                    print "Input Text Cleaner: " + word_cleaner
                RunSingleTest(word_cleaner, corpus_freq, acronym_path, verbose)

if __name__ == "__main__": main()
    
    