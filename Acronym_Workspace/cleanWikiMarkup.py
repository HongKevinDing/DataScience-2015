# -*- coding: utf-8 -*-

## CDIPS 2015 Workshop Project
## Team: Acronyms
## Members: Hong Ding, Philipp Dumitrescu, Herman Leung
## July 11 - Aug 1, 2015

'''
The cleanWikiMarkup() function takes a text string in Wiki markup and
    returns a text string where all markup is removed.

    Two steps are involved:

    (1) First, it uses regex to clean up all Wiki markup in a string
        except for curly brackets {}

    (2) The second part uses the functions get_reducer_ranges() and
        apply_excise_list_to_text() to remove curly brackets and their contents.
        These two functions circumvent the difficulty of using solely regex to
        deal with nested brackets. They essentially find the indices of all
        curly brackets in the string, and iteratively deletes the closest pair
        of open and close curly brackets and everything in between, ensuring
        that only the innermost pairs of brackets are deleted first.
'''

import re
import numpy as np


def get_reducer_ranges(braces_list_signed, braces_list_positions, length_of_braces):
    marker = 0
    excise_list = np.zeros([1,2], dtype='i4')
    temp_touple = np.array([0,0])
    if (len(braces_list_signed) != len(braces_list_positions)):
        print "Lists of Unequal Lengths. Return Empty!"
        return
    for i in range(0, len(braces_list_signed)):
        if(marker == 0):
            temp_touple[0] = braces_list_positions[i]
        marker += braces_list_signed[i]
        if(marker == 0):
            temp_touple[1] = braces_list_positions[i] + length_of_braces
            excise_list = np.append(excise_list, [temp_touple], axis=0)
    if (marker != 0):
        print "Marker did not get back to zero indicating unpaired brackets!"
        return
    return excise_list

def apply_excise_list_to_text(excise_list,oldstring):
    newstring = ''
    if excise_list != None:
        for i in range(0,len(excise_list)-1):
            newstring += oldstring[excise_list[i,1]:excise_list[i+1,0]]
        newstring += oldstring[excise_list[len(excise_list)-1,1]:]
        return newstring
    else:
        return oldstring


def cleanWikiMarkup(text):

    '''Part 1: Clean all markup except for {{}}'''

    RE_BRACKETS = re.compile(r'{{(?:.(?!{{|}}).)*}}')#  {{}} and everything inside as long as there are no nested {{}}
    RE = re.compile(r'''\[{2}(File|Category):.+?\]{2}|        #  [[File: ]]
                                    [\s\w#()]+?\||            #
                                    (\[{2}|\]{2})|            #  [[ or ]]
                                    \'{2,5}|                  #  two to five occurences of '
                                    (<s>|<!--).+?(</s>|-->)|  #  comments
                                    ={1,6}|                   #  one to six occurences of =
                                    \<ref.+?(\/>|\<\/ref\>)|  #  <ref /> and <ref></ref> tags
                                    \<.+?\>                   #  any tags
                                    ''',
                                    re.X)
      # The above regular expression was adopted from daddyd's dewiki parser.py
      # http://github.com/daddyd/dewiki/blob/master/dewiki/parser.py

    text = re.sub(RE, ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub('\( ', '(', text)
    text = re.sub(' \)', ')', text)
    text = re.sub('\|', '| ', text)
    text = re.sub(' \.', '.', text)

    '''Part 2: Clean {{}}'''

    braces_list_signed = re.findall('{{|}}', text)
    braces_list_signed = [+1 if brace == '{{' else -1 for brace in braces_list_signed]
    braces_list_positions = [m.start(0) for m in re.finditer('{{|}}', text)]
    excise_list = get_reducer_ranges(braces_list_signed, braces_list_positions, 2)
    text = apply_excise_list_to_text(excise_list, text)

    return text
