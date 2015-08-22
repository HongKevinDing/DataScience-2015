# DataScience-2015 Readme
#####Our team consisted of Hong Ding, Philipp Dumitrescu and Herman Leung. Under the mentorship of Hossein Falaki from Databricks, we devoted three weeks during the summer of 2015 working on an exploratory project in named entity recognition of acronyms.

#####Our overarching vision for the project was to create a text processing engine that can identify the meaning of an acronym in any text. We approached the project by dividing it into two parts: 

#####(1) Acronym recognition, extraction, and analysis
#####(2) Acronym disambiguation

#####The first part involved using regular expressions to scrape and extract acronyms and acronym-definition pairs from AcronymFinder.com and Wikipedia. Then we did exploratory analysis on the extracted data, such as comparing letter frequencies of the acronyms between the two sites, frequency of acronyms in Wikipedia pages, characteristics that might distinguish acronyms from regular English words, etc.

#####The second part involved two parts itself: building a test corpus and building algorithms for disambiguating acronyms on the test corpus.

#####For the corpus, we picked 50 acronyms each with (at least) two potential meanings. We obtained all the text from the Wikipedia pages for each meaning per acronym, and converted them into bags of words (word frequency dictionaries). We also grabbed texts randomly from non-Wikipedia webpages for one of the two meanings for each of the 50 acronyms and bagged the words as well; these served as preliminary test data for our acronym disambiguation algorithms.

#####For the disambiguation algorithm, we used word frequencies in the texts and weighted them by word frequencies in the English language (where rarer words get higher scores), then compared the overlap between the Wikipedia word frequencies for each meaning against the non-Wikipedia one, returning two scores that indicate “match” and that can be ranked and used for deciding which of the two meanings the acronym in the non-Wikipedia text stands for.

#####Since this project is exploratory in nature, much work remains to be done to see the original goal of the project come to fruition. The files in this repository reflect the exploratory work we have done. We have aimed to make our code bug-free but it is by no means intended to be in a state for public, out-of-the-box usage.

