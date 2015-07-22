# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:02:22 2015

@author: Philipp Dumitrescu
"""
import json
import os
import glob
import copy
import surrounding_words_metrics as my_metrics
import dictionary_stemmer


test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'Testing','50','cleaned')

print test_dir

list_of_cleans = ["unstemmed", "porter", "lancaster", "wordnet", "allwords"]

if "1" in ["1"]:
    #fp_englang_json = open('./Word_Frequency/Word_Count/ANC_count.json')
    fp_englang_json = open('./Word_Frequency/Word_Count/Beautiful_Data.json')

    my_englang_count = json.load(fp_englang_json) 
    fp_englang_json.close()
    my_englang_totalcount = my_metrics.AddCounts(my_englang_count)
    #print my_englang_totalcount
    #print len(my_englang_count.values())
    my_englang_freq = copy.deepcopy(my_englang_count)
    my_metrics.MapCountToFreq(my_englang_freq, my_englang_totalcount)
    #print my_englang_count["test"]
    #print my_englang_freq["test"]
    my_englang_info = copy.deepcopy(my_englang_freq)
    my_metrics.FequenciesToInformation(my_englang_info)
    #print my_englang_info.nr


for word_cleaner in list_of_cleans:
    
    stemmed_dictionary = dictionary_stemmer.stem_dict(my_englang_freq, word_cleaner)

    success = 0
    fail   = 0
    clean_dir = os.path.join(test_dir, word_cleaner)
    print clean_dir
    subfolder_names =  [name for name in os.listdir(clean_dir)
            if os.path.isdir(os.path.join(clean_dir, name))]
    for acronym in subfolder_names:
        acronym_dir = os.path.join(clean_dir, acronym)
        #Load Three Jason Files
        words0 = json.load(open(os.path.join(acronym_dir,'0.json')))
        words1 = json.load(open(os.path.join(acronym_dir,'1.json')))
        wordsP = json.load(open(os.path.join(acronym_dir,'paragraph.json')))
        
        words0_TotalCounts = my_metrics.AddCounts(words0)
        words1_TotalCounts = my_metrics.AddCounts(words1)
        wordsP_TotalCounts = my_metrics.AddCounts(wordsP)
        
        
        my_metrics.MapCountToFreq(words0,words0_TotalCounts)
        my_metrics.MapCountToFreq(words1,words1_TotalCounts)
        my_metrics.MapCountToFreq(wordsP,wordsP_TotalCounts)
        
        contrib0 = {}
        contrib1 = {}

        metric0 = my_metrics.SimplestMetricWighted(wordsP,words0, my_englang_freq, contrib0)
        metric1 = my_metrics.SimplestMetricWighted(wordsP,words1, my_englang_freq, contrib1)
        
        if(metric0 > metric1):
            guess = '0'
        else:
            guess = '1'
        if os.path.exists(os.path.join(acronym_dir, 'Answer_0')):
            ref_answer = '0'
        elif os.path.exists(os.path.join(acronym_dir, 'Answer_1')):
            ref_answer = '1'
        else:
            'FAIL: Could not find answer file.'
        
        if (guess == ref_answer):
            success +=1
#            test_ratio = metric0/metric1 if (guess=='0') else metric1/(metric0 + 1e-16)
#            print "%8s : 0: %10.4e, 1: %10.4e, rightness: %6.2f" % (acronym, metric0, metric1, test_ratio)

        else:
            fail += 1
            test_ratio = metric0/metric1 if (guess=='0') else metric1/metric0
            print "%8s : 0: %10.4e, 1: %10.4e, wrongness: %6.2f" % (acronym, metric0, metric1, test_ratio)
    print success
    print fail
    print fail / 50.0

        

    #print glob.glob(os.path.join(clean_dir,'*'))
   # for 
    