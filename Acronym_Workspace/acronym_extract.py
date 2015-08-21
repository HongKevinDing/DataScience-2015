# -*- coding: utf-8 -*-

## CDIPS 2015 Workshop Project
## Team: Acronyms
## Members: Hong Ding, Philipp Dumitrescu, Herman Leung
## July 11 - Aug 1, 2015

'''
This code takes a (large text) string and extracts acronyms along with their definitions,
in either of these forms:
    - University of California, Berkeley (UCB)
    - UCB (University of California, Berkeley)

There are four possible outputs - see inside function for details.
'''

import re

def extract_acronym(text, search='complex', surrounding='F'):

    if search in ['reduced1', 'reduced2']:
        surrounding = 'F'   # the 'reduced' and 'simple' options should never
                            # include surrounding words (i.e. surrounding='F')

    # 'complex' = returns list of lists of acronyms with definitions
                  # Returns: [['acronym', 'definition',
                  #            'surrounding words (up to 2000 max)'], [], ...]
    # 'reduced2' = list of tuples of (acronyms + definitions, counts)
                  # Returns: [(acronym_definition, counts),
                  #           (acronym_definition2, counts2), ...]
    # 'reduced1' = list of tuples of (acronyms, counts)
                  # Returns: [(acronym, counts), (acronym2, counts2), ...]
                  # * NOTE * ignores definitions
                  # * NOTE * uses the more complicated definition of acronyms
                  #          (in parentheses or followed by parentheses)
    # 'simple' = grabs all acronyms (bare or in parentheses) without
                  # definitions or surrounding words
                  # Returns: [(acronym, counts), (acronym2, counts2), ...]

    '''
    The 'simple' version
    uses a very barebones definition of acronyms:

         - Anything in capital letters more than 1 character long,
           optionally with periods after each character (which will be
           deleted and counted as the same as without periods)

    The 'reduced1', 'reduced2', and 'complex' versions
    use the following definition for acronyms:

         1. composed of upper case alphabetic characters only
               (except optionally with periods after each char)

         2. at least 2 chars long
               (but not one capital letter followed by a period)

         3. in parentheses, or followed by parentheses
               (original 'long' form preceding the acronym, or inside
                parentheses after the acronym)

         4. the definition (i.e., the original "long" form) of the acronym
               must begin with a capital letter identical to that of the acronym
               (e.g., 'bachelor of arts (BA)' would not be picked up,
                      because 'bachelor' is lowercase)

         5. the definition has at least as many words as letters in the acronym,
               and at most the number of letters in the acronym + 4 more words
               (to account for function words that often don't get represented
                in the acronym)
               (e.g., 'community integration (COMINT)' would not be picked up,
                      because words in definition < letters in acronym)

    '''
    acronym_list = []

    if search == 'simple':
        acro_list = re.findall('[A-Z]{2,}|(?:[A-Z]\.){2,}', text)
        acro_list = [re.sub('\.', '', a) for a in acro_list]
        acro_dict = {}
        for a in acro_list:
            if a not in acro_dict.keys():
                acro_dict[a] = 1
            else:
                acro_dict[a] += 1
        acronym_list = list(acro_dict.items())

    else:
        if re.search('[A-Z]{2,} \(|\([A-Z]{2,}\)', text) == None:
            pass

        else:
            text = re.sub('\s+', ' ', text)
            text_list = text.split(' ')

            LEN = len(text_list)

            for i in range(LEN):
                acronym = None
                definition = None
                surrounding_words = []
                STRING = text_list[i]

                # 1. Only look at strings that are at least 2 chars long
                if len(STRING) > 1:

                    # 1.1. Get definition

                    # 1.1.1 ignore if there is lowercase, parentheses, or period
                    if re.search('[^A-Z\(\)\.]', STRING):
                        pass

                    # 1.1.2. else if there is an open parenthesis
                    elif STRING[0] == '(' and STRING[-1] == ')':
                        if len(STRING) > 3:
                            acronym = STRING[1:-1]
                            # if STRING[-1] == ')':  # if there is a close paren
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
                                               # not longer than acronym
                                               # position in list, because we're
                                               # going to search the preceding
                                               # words in order to grab the
                                               # "definition" of the acronym

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
                                            (word[0] == acronym[0])):   # first character is the same between acronym and word

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
                    if surrounding == "T" and definition != None:
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
                    4. if search = "reduced1" or "reduced2", reduce acronym_list by count
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
                    if surrounding == 'T':
                        acronym_list.append([acronym, definition, surrounding_words])
                    elif surrounding == 'F':
                        if search == 'reduced2':
                            acronym_list.append(str(acronym) + ' - ' + str(definition))
                        else:
                            acronym_list.append([acronym, definition])

                if search == "reduced1":
                    acro_dict = {}
                    for a in acronym_list:
                        if a[0] not in acro_dict.keys():
                            acro_dict[a[0]] = 1
                        else:
                            acro_dict[a[0]] += 1
                    acronym_list = list(acro_dict.items())

            if search == "reduced2":  # this block is outdented from previous
                                      # block for a very good reason
                acro_dict = {}
                for a in acronym_list:
                    if a not in acro_dict.keys():
                        acro_dict[a] = 1
                    else:
                        acro_dict[a] += 1
                acronym_list = list(acro_dict.items())

    return acronym_list
