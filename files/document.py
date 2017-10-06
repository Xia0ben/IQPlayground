from collections import Counter
from math import log10
import re

from nltk import word_tokenize

'''
Document class

author :Alexis Fossart
date :  06/10/2017

Class used to represent a document in memory
'''


class Document:
    def __init__(self, xml_text, ignore_case= True):
        text = re.sub("<[^>]*>", "", xml_text)
        if ignore_case:
            text = text.lower()
        self.__tokens = word_tokenize(text)
        self.__counter = Counter(self.__tokens)

    def __str__(self):
        ret = "Number of tokens : {}\nFirst 20 tokens :\n{}".format(len(self.__tokens), self.__tokens[:20])
        return ret

    def set_of_terms(self):
        return set(self.__tokens)

    def doc_id(self):
        return self.__tokens[0]

    def term_frequecy(self, term):
        if term in self.__counter:
            return 1 + log10(self.__counter[term])
        else:
            return 0