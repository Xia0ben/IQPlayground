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
        '''
        Init of the document
        :param xml_text: xml text representing the document
        :param ignore_case: should we convert the xml to lower case ?
        '''
        text = re.sub("<[^>]*>", "", xml_text)
        if ignore_case:
            text = text.lower()
        self.__tokens = word_tokenize(text)
        self.__counter = Counter(self.__tokens)

    def __str__(self):
        ret = "Number of tokens : {}\nFirst 20 tokens :\n{}".format(len(self.__tokens), self.__tokens[:20])
        return ret

    def set_of_terms(self):
        '''
        :return: a set of the tokens in the document
        '''
        return set(self.__tokens)

    def doc_id(self):
        '''
        here we use the fact that the first token is always the docid in the documents of our corpus
        :return: the docid of the document
        '''
        return self.__tokens[1]

    def term_frequecy(self, term):
        '''
        return the term-frequency of a term
        slide 8 : tf(t,d) = 1 + log(nt,d) or 0 if nt,d = 0
        :param term: the term for wich we seek the frequency
        :return: the term-frequency of the term
        '''
        if term in self.__counter:
            return 1 + log10(self.__counter[term])
        else:
            return 0