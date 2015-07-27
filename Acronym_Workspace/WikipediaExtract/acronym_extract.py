# -*- coding: utf-8 -*-

# CDIPS 2015 Project
# Team: Kevin Ding, Philipp Dumitrescu, Herman Leung

'''
This code takes a (large text) string and returns a list of lists:
[['acronym', 'definition', 'surrounding words (up to 2000 max)'], [], ...]
'''

import re

def extract_acronym(text):
    '''
    This function takes a string and returns a list of lists:
    [['acronym', 'definition', 'surrounding words (up to 2000 max)'], [], ...]
       -string-    -string-      -list-

    It uses a 'simple' definition for acronyms:

         1. composed of upper case alphabetic characters only
               (except optionally with periods after each char)

         2. at least 2 chars long
               (but not one capital letter followed by a period)

         3. in parentheses, or followed by parentheses
               (original 'long' form preceding, or inside parentheses after)

         4. the definition (i.e., the original "long" form) of the acronym
               must begin with a capital letter identical to that of the acronym
               (e.g., 'bachelor of arts (BA)' would not be picked up,
                      because 'bachelor' is lowercase)

         5. the definition has at least as many words as letters in the acronym,
               at most number of letters in the acronym + 4 more words
               (to account for function words that often don't get represented in the acronym)
               (e.g., 'community integration (COMINT)' would not be picked up,
                      because number of words in definition < number of letters in acronym)

    '''
    text = re.sub('\s+', ' ', text)
    text_list = text.split(' ')

    acronym_list = []
    LEN = len(text_list)

    for i in range(LEN):
        acronym = None
        definition = None
        surrounding_words = []
        STRING = text_list[i]

        # 1. Only look at strings that are at least 2 chars long
        if len(STRING) > 1:

            # 1.1. Get definition

            # 1.1.1 ignore if there are chars that are not capital, parentheses, or period
            if re.search('[^A-Z\(\)\.]', STRING):
                pass

            # 1.1.2. else if there is an open parenthesis
            elif STRING[0] == '(' and STRING[-1] == ')':
                if len(STRING) > 3:
                    acronym = STRING[1:-1]
                    # if STRING[-1] == ')':   # if there is a close paren
                    #     acronym = STRING[1:-1]
                    # else:                      # if there isn't a close paren
                    #     acronym = STRING[1:]   #   (sometimes an acronym in parentheses have other
                    #                            #    information on the acronym before the close paren,
                    #                            #    e.g., pronunciation, especially on Wikipedia)

                    if re.search('([A-Z]\.){2,}', acronym) and len(acronym)%2 == 0:
                        acro_len = int(len(acronym)/2)
                    elif '.' in acronym:
                        break
                    else:
                        acro_len = len(acronym)

                    if acro_len <= i:  # check that acronym length is
                                       # not longer than acronym position in list
                                       # because we're going to search the
                                       # preceding words in order to grab
                                       # the "definition" of the acronym

                        if i - acro_len <= 0:
                            START = 0
                        else:
                            START = i - acro_len

                        if START - 4 < 0:
                            STOP = -1
                        else:
                            STOP = START - 5

                        ## First check if the number of words before acronym (that equal number of letters in acronym)
                        ## have the same sequence of initial letters as the letters in the acronym
                        words_before_acronym = [re.sub('\"', '', text_list[m]) for m in range(i-acro_len, i, 1)]
                        initials_before_acronym = ''.join([word[0] for word in words_before_acronym]).upper()
                        if initials_before_acronym == acronym:
                            definition = ' '.join(words_before_acronym)

                        # reverse look back, up to (acronym length + 4) word slots before acronym
                        else:
                            for j in range(START, STOP, -1):
                                word = re.sub('\"', '', text_list[j])
                                if ((word[-1] not in '.!?\"\)\;\:') and   # not last word of a previous sentence and word not in parentheses
                                    (word[0] == acronym[0])):   # first character is the same between
                                                                                # acronym and word
                                    if '(' not in ' '.join(text_list[j:i]):
                                        definition = ' '.join(text_list[j:i])
                                        break
                                    else:      # if parentheses in definition, then grab from word after close parenthesis and check its first letter
                                        for k in range(START, i, 1):
                                            word = re.sub('\"', '', text_list[k])
                                            if word[-1] == ')':
                                                if text_list[k+1][0] == acronym[0]:
                                                    definition = ' '.join(text_list[k+1:i])
                                                    break

            # 1.1.3 else if there aren't parentheses (look for definition in parentheses after the acronym)
            elif not re.search('[\(]', STRING) and i != LEN-1:
                acronym = STRING
                word_after = text_list[i+1]
                if i == LEN - 1:    # if word is the last one in the list, pass
                    pass
                elif (word_after[0] == '(' and       # if word after acronym starts with '('
                      word_after[1] == acronym[0]):   # and first letters match
                    if re.search('([A-Z]\.){2,}', acronym):
                        acro_len = int(len(acronym)/2)
                    else:
                        acro_len = len(acronym)
                    if i + acro_len + 4 <= LEN:
                        STOP = i + acro_len + 4
                    else:
                        STOP = LEN
                    for j in range(i+1, STOP, 1):
                        word = text_list[j]
                        if word[-1] == ')':
                            definition = ' '.join(text_list[i+1:j+1])
                            definition = re.sub('[\(\)\"]', '', definition)
                            break

            # 1.2. Get surrounding words
            if definition != None:
                if i < 1000:
                    START = 0
                else:
                    START = i - 1000
                if i + 1000 > LEN:
                    STOP = LEN
                else:
                    STOP = i + 1000
                surrounding_words = text_list[START:STOP]

        ''' Some final checks
            1. delete periods from acronyms
            2.1 make sure the exact same acronym doesn't appear in the definition
            2.2 make sure initials in acronym occur in sequential order in definition
            3. make sure objects 'acronym' and 'definition' have values
        '''
        if acronym != None and '.' in acronym:
            acronym = re.sub('.', '', acronym)

        if acronym != None and definition != None:
            acronym_chars = [char for char in acronym]
            CHECK_INITIALS = re.compile(''.join([str(char + '.*?') for char in acronym_chars]))
            if not re.search(CHECK_INITIALS, definition) or re.search(acronym, definition):
                acronym = None
                definition = None

        if acronym not in [None, [], ''] and definition not in [None, [], '']:
            acronym_list.append([acronym, definition, surrounding_words[0]])

    return acronym_list
