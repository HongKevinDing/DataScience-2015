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
import math
import json


def FequenciesToInformation(in_dictionary_freq):
    """
    This function takes the probabilites and maps them to information content.
    """
    for key,value in english_lang_freq.iteritems():
        value = math.log (1.0 / value)
    return in_dictionary_info

def CountsToFrequencies(in_dictionary_counts):
    for pair in english_lang_freq:
        in_dictionary_frequs = in_dictionary_counts / nr_of_words



def WeightWordsFrequecyByInformation(my_dict_info, english_lang_info):
    for key, value in my_dict:
        value abs(my_dict_info - english_lang_info)


# Considerations cutoff of noise


# Weighted: Rare words produce less of an impact than common words 
def SimplestMetricWighted(my_dict_freq, compare_to_dict_freq):
    metric = 0.0
    for key, value in my_dict_freq.iteritems():
        metric += value  * abs(log_2(compare_to_dict_freq[key] / value)) * (1.0 / english_lang_info[key])
    return metric
    
# No weighting in the one below. Sort according to lowest ones
def SimplestMetric(my_dict_freq, compare_to_dict_freq):
    metric = 0.0
    for key, value in my_dict_freq.iteritems():
        metric += value  * abs(log_2(compare_to_dict_freq[key] / value))
    return metric 
     
def PlotWordDistributionOfText():
    suff
    
    
# -----
    
def main():
    fp_englang_json = open()
    my_englang = json.load(fp_englang_json) 
    fp_englang_json.close()
    print fp_englang_json
    
if __name__ == "__main__": main()