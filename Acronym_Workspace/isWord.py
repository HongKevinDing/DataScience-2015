## CDIPS 2015 Workshop Project
## Team: Acronyms
## Members: Hong Ding, Philipp Dumitrescu, Herman Leung
## July 11 - Aug 1, 2015

''' The isWord() function checks whether the input (an acronym)
    is a word according to the Carnegie Mellon University Pronouncing Dictionary (cmudict)
    As of July 2015, cmudict has 123,455 words.

    The isPalindrome() function checks whether the input (an acronym)
    is a palindrome (e.g., ABBA, CATAC)

    The hasRepeatedLetter() function checks whether there
    are any repeating letters at all in the input (an acronym)
'''

from nltk.corpus import cmudict

cmulist = cmudict.dict().keys()

# These are needed to make processing much faster
cmu_oneletter = [word for word in cmulist if len(word) == 1]
cmu_first2 = list(set([word[:2] for word in cmulist]))   # list of first 2 chars
cmu_first3 = list(set([word[:3] for word in cmulist]))   # list of first 3 chars


def isWord(string):
    STRING = str(string).lower()
    LEN = len(STRING)
    if LEN == 1 and STRING in cmu_oneletter:
        return 1
    elif LEN == 2:
        if STRING in cmu_first2:
            if STRING in cmu_list:
                return 1
            else:
                return 0
        else:
            return 0
    elif LEN == 3:
        if STRING in cmu_first3:
            if STRING in cmu_list:
                return 1
            else:
                return 0
        else:
            return 0
    else:
        if STRING[:3] in cmu_first3:
            if STRING in cmu_list:
                return 1
            else:
                return 0
        else:
            return 0


def isPalindrome(string):
    STRING = str(string).lower()
    LEN = len(STRING)
    if LEN < 2:
        return 0
    elif LEN == 2 or LEN == 3:
        if STRING[0] == STRING[-1]:
            return 1
        else:
            return 0
    else:
        if STRING[0] == STRING[-1]:
            if LEN%2 == 0:
                FIRSTHALF = STRING[:int(LEN/2)]
                SECONDHALF = [STRING[i] for i in range(LEN-1, int(LEN/2-1), -1)]
                if FIRSTHALF == SECONDHALF:
                    return 1
                else:
                    return 0
            else:
                FIRSTHALF = STRING[:int(LEN//2)]
                SECONDHALF = [STRING[i] for i in range(LEN-1, int(LEN//2), -1)]
                if FIRSTHALF == SECONDHALF:
                    return 1
                else:
                    return 0
        else:
            return 0


def hasRepeatedLetter(string):
    STRING = str(string).lower()
    STRING_DICT = {}
    for s in STRING:
        if s not in STRING_DICT.keys():
            STRING_DICT[s] = 1
        else:
            STRING_DICT[s] += 1
    if len(STRING_DICT.values()) == len(STRING):
        return 0
    else:
        return 1
