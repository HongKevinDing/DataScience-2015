## CDIPS 2015 Workshop Project
## Team: Acronyms
## Members: Hong Ding, Philipp Dumitrescu, Herman Leung
## July 11 - Aug 1, 2015

''' Data preprocess for bootstrapping and comparing frequency distributions
    between two (or more) sets of unique acronyms.

    This file takes some large list of at least 50k unique acronyms,
    randomly picks (with replacement) 227 of the acronyms,
    creates a letter count dictionary out of them,
    and optionally turns the counts to percentages (freqtype argument),
    then writes that sample to a line in a csv file.

    At present, the code takes 5000 samples (global object R).
'''

import lists_and_dicts as ld
import numpy as np
import operator, re

AF = ld.AF_set_list2        # AcronymFinder acronyms list (~ 300K)
Wiki = ld.acro_set_list     # Wikipedia acronyms list (~ 50 K)
Diff = ld.difference2       # List of acronyms that are found in Wikipedia but not AcronymFinder (~ 6K)

# Make sure every item in the lists are strings, and make sure they are entirely consisted of
# capital English letters only (A-Z).

AF = [A for A in AF if type(A) == str]
Wiki = [k for k in Wiki if type(k) == str and re.search('[^A-Z]', str(k)) == None]
Diff = [D for D in Diff if type(D) == str]

def list_to_string(LIST):
    ''' Joins all the strings in the list
        and returns one big string
    '''
    newstring = ''
    for L in LIST:
        newstring += str(L)
    return newstring

def string_to_dict(string):
    ''' Creates letter frequency dictionary
        out of a string
    '''
    newdict = {}
    for s in string:
        if s not in newdict.keys():
            newdict[s] = 1
        else:
            newdict[s] += 1
    return newdict

def dict_to_string(DICT, freqtype="rawcount"):
    ''' Takes all values in a dictionary
        and returns a comma-separated string of the values,
        with option to convert the values to frequency
    '''
    newstring = ''
    newlist = list(DICT.values())
    if freqtype == 'percent':
        newlist = [float(item)/sum(newlist) for item in newlist]
    for n in newlist:
        newstring += str(n) + ','
    newstring = newstring[:-1]
    return newstring

R = 5000  # samples to bootstrap

def write_to_csv(LIST, DIR_WRITE, freqtype="rawcount"):
    ''' Writes/appends the string of comma-separated values
        into a csv file.
    '''
    with open(DIR_WRITE, 'w') as f:
        f.write('')
    for i in range(R):
        sample_list = np.random.choice(LIST, size=227, replace=True)
        sample_string = list_to_string(sample_list)
        sample_dict = string_to_dict(sample_string)
        if freqtype == "rawcount":
            printstring = dict_to_string(sample_dict)
        elif freqtype == "percent":
            printstring = dict_to_string(sample_dict, "percent")
        with open(DIR_WRITE, 'a') as f:
            f.write('\n' + printstring)

DIR = '/Users/herman/Documents/CDIPS-DSW-2015/DataScience-2015_self/'

write_to_csv(AF, DIR + 'AF_bootstrap_counts.csv')
write_to_csv(Wiki, DIR + 'Wiki_bootstrap_counts.csv')
write_to_csv(Diff, DIR + 'Diff_bootstrap_counts.csv')

write_to_csv(AF, DIR + 'AF_bootstrap_percent.csv', "percent")
write_to_csv(Wiki, DIR + 'Wiki_bootstrap_percent.csv', "percent")
write_to_csv(Diff, DIR + 'Diff_bootstrap_percent.csv', "percent")
