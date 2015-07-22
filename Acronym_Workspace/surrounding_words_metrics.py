# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:02:22 2015

@author: Philipp Dumitrescu

Takes two dictionaries of words : count and produces a ranking based on the 
overlap between them.


Input :

my_dict = {"words" : count}
    words and count from the text surrounding the acronym
compare_to_dict = {"words" : count}
    words and count from article we are trying to compare to.  

english_lang_freq : frequency of words in the english language
"""
import copy
import math
import json
import matplotlib.pyplot as plt

def AddCounts(my_dict_cout):
    count = 0
    for value in my_dict_cout.itervalues():
        count += value
    return count

def MapCountToFreq(english_lang_freq, my_englang_totalcount):
    for key, value in english_lang_freq.iteritems():
        english_lang_freq[key] *= 1.0 / (my_englang_totalcount)
    return

def FequenciesToInformation(in_dictionary_freq):
    for key, value in in_dictionary_freq.iteritems():
        in_dictionary_freq[key] = math.log (1.0 / value)
    return

#def WeightWordsFrequecyByInformation(my_dict_info, english_lang_info):
#    for key, value in my_dict:
#        value abs(my_dict_info - english_lang_info)
#

# Considerations cutoff of noise

# No stopwords -- no meaning attached to them



# Weighted: Rare words produce less of an impact than common words 
def SimplestMetricWighted(my_dict_freq, compare_to_dict_freq, english_lang_freq, test_paragraph_UCBerk_metric_contrib):
    overlap = 0.0
    for key, value in my_dict_freq.iteritems():
        if(key in compare_to_dict_freq):
            if(key in english_lang_freq):
                key_overlap_contrib = abs(compare_to_dict_freq[key] * value) * (1.0 + 1.0 / float(english_lang_freq[key]))
            else:
                key_overlap_contrib = abs(compare_to_dict_freq[key] * value) 
            overlap += key_overlap_contrib
            test_paragraph_UCBerk_metric_contrib[key] = key_overlap_contrib
        else:
            test_paragraph_UCBerk_metric_contrib[key] = 0
    return overlap

def SimplestMetricWighted(my_dict_freq, compare_to_dict_freq, english_lang_freq, test_paragraph_UCBerk_metric_contrib):
    overlap = 0.0
    for key, value in my_dict_freq.iteritems():
        if(key in compare_to_dict_freq):
            if(key in english_lang_freq):
                key_overlap_contrib = abs(compare_to_dict_freq[key] * value) * (1.0 / float(english_lang_freq[key]))
            else:
                key_overlap_contrib = abs(compare_to_dict_freq[key] * value) 
            overlap += key_overlap_contrib
            test_paragraph_UCBerk_metric_contrib[key] = key_overlap_contrib
        else:
            test_paragraph_UCBerk_metric_contrib[key] = 0
    return overlap
    
# No weighting in the one below. Sort according to lowest ones
def SimplestMetric(my_dict_freq, compare_to_dict_freq):
    metric = 0.0
    for key, value in my_dict_freq.iteritems():
        metric += value  * abs(math.log(compare_to_dict_freq[key] / value))
    return metric 
     
def PlotKeysHistogram(my_englang_info):
     
    
    return
    

# Plot: def information content of words
# -----
    
def main():
    fp_englang_json = open('../Word_Frequency/Word_Count/ANC_count.json')
    my_englang_count = json.load(fp_englang_json) 
    fp_englang_json.close()
    my_englang_totalcount = AddCounts(my_englang_count)
    #print my_englang_totalcount
    #print len(my_englang_count.values())
    my_englang_freq = copy.deepcopy(my_englang_count)
    MapCountToFreq(my_englang_freq, my_englang_totalcount)
    #print my_englang_count["test"]
    #print my_englang_freq["test"]
    my_englang_info = copy.deepcopy(my_englang_freq)
    FequenciesToInformation(my_englang_info)
    #print my_englang_info.nr
    
    test_website_UCBank = json.load(open('../Testing/UCBank2.json'))
    test_website_UCBerk = json.load(open('../Testing/UCBerkeley2.json'))
    test_paragraph_UCBerk = json.load(open('../Testing/UCBerkeley_new2.json'))

    contrib0 = {}
    contrib1 = {}

    test_website_UCBank_counts = AddCounts(test_website_UCBank)
    test_website_UCBerk_counts = AddCounts(test_website_UCBerk)
    test_paragraph_UCBerk_counts = AddCounts(test_paragraph_UCBerk)
    
    MapCountToFreq(test_website_UCBank,test_website_UCBank_counts)
    MapCountToFreq(test_website_UCBerk,test_website_UCBerk_counts)
    MapCountToFreq(test_paragraph_UCBerk,test_paragraph_UCBerk_counts)

    print SimplestMetricWighted(test_paragraph_UCBerk,test_website_UCBank, my_englang_freq, contrib0)
    print SimplestMetricWighted(test_paragraph_UCBerk,test_website_UCBerk, my_englang_freq, contrib1)

    import operator
    sorted_0 = sorted(contrib0.items(), key=operator.itemgetter(1))
    sorted_1 = sorted(contrib1.items(), key=operator.itemgetter(1))

    #print sorted_0
    #print sorted_1

    fp_out_berkeley = open("berkeley_out.json", "w")
    fp_out_bank     = open("bank_out.json", "w")

    json.dump(sorted_0, fp_out_bank)
    json.dump(sorted_1, fp_out_berkeley)
    
   # print test_paragraph_UCBank
    #print test_paragraph_UCBerk
    
    
    #my_englang_count - 
    
    #PlotKeysHistogram(my_englang_info);
    

    
if __name__ == "__main__": main()