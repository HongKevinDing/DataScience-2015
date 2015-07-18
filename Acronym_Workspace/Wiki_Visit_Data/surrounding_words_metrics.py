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
def SimplestMetricWighted(my_dict_freq, compare_to_dict_freq):
    metric = 0.0
    for key, value in my_dict_freq.iteritems():
        metric += abs(compare_to_dict_freq[key] * value) * (1.0 / english_lang_info[key])
    return metric
    
# No weighting in the one below. Sort according to lowest ones
def SimplestMetric(my_dict_freq, compare_to_dict_freq):
    metric = 0.0
    for key, value in my_dict_freq.iteritems():
        metric += value  * abs(log_2(compare_to_dict_freq[key] / value))
    return metric 
     
def PlotKeysHistogram():
    
    

# Plot: def information content of words
# -----
    
def main():
    fp_englang_json = open('../Word_Frequency/Word_Count/ANC_count.json')
    my_englang_count = json.load(fp_englang_json) 
    fp_englang_json.close()
    my_englang_totalcount = AddCounts(my_englang_count)
    print my_englang_totalcount
    my_englang_freq = copy.deepcopy(my_englang_count)
    MapCountToFreq(my_englang_freq, my_englang_totalcount)
    print my_englang_count["test"]
    print my_englang_freq["test"]
    my_englang_info = copy.deepcopy(my_englang_freq)
    FequenciesToInformation(my_englang_info)
    print my_englang_info.values()
    
    PlotKeysHistogram(my_englang_info);
    

    
if __name__ == "__main__": main()