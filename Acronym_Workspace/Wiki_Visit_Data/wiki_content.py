import re
from wikipedia import WikipediaPage
import wikipedia

class WikiAcronym():
    def __init__(self,acr_str,lower_case=True):
        try:
            self._WikiPage = WikipediaPage(title=acr_str)
            self._valid = True
        except:
            self._valid = False
        self._acroynom = acr_str
        self._upper = list(self._acroynom.upper())
        self._lower = list(self._acroynom.lower())
        self.pattern =None

    def patern_gen(self):
        pattern = r"^"
        for i in range(len(self._upper)):
            pattern+='['+self._upper[i]+'|'+self._lower[i]+'].*'
        pattern+='$'
        self.pattern=pattern


    def acro_list(self):

        results= []
        if self.pattern == None:
            self.patern_gen()
        try:
            if len(self._WikiPage.acronym) > 0:
                results =[entry for entry in self._WikiPage.acronym if re.search(self.pattern, entry)]
        except:
            pass
        return results


def main():

    string = 'UCB'
    u = WikiAcronym(string)
    if u._valid:
        for k in u.acro_list():
            try:
                page = wikipedia.summary(k,sentences=10)
                print page
            except:
                print k, 'cannot getit'
# display some lines

if __name__ == "__main__": main()
'''
pattern_comp = r"^[U|u].*[C|c].*[B|b].*$"
print pattern_comp
'''