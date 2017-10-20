from collections import Counter
from math import log10
import re

'''
Document class

author :Belgharib Zakaria
date :  12/10/2017

Class used to represent a document in memory
'''

'''
title weight : tw
date weight : dw
'''
tw = 10
dw = 2

class Document2:

    def __init__(self, xml_text, ignore_case= True):
        '''
        Init of the document
        :param xml_text: xml text representing the document
        :param ignore_case: should we convert the xml to lower case ?
        '''
        text = re.sub("", "", xml_text)
        if ignore_case:
            text = text.lower()
        self.__tokens_title = []
        self.__tokens_date = []
        self.__tokens_neutral = []
        type_t = ""
        for token in text.split():
            if token.lower() == "<title>":
                type_t="title"
            elif token.lower() == "<date>":
                type_t="date"
            elif token.lower() == "</title>" or token.lower() == "</date>":
                type_t=""
            else:
                if type_t == "title":
                    self.__tokens_title.append(token)
                elif type_t == "date":
                    self.__tokens_date.append(token)
                else:
                    if token.lower()[0] != "<" and token.lower()[-1] != ">":
                        self.__tokens_neutral.append(token)

        self.__counter_neutral = Counter(self.__tokens_neutral)
        self.__counter_title = Counter(self.__tokens_title)
        self.__counter_date = Counter(self.__tokens_date)
        print(self.__counter_neutral)
        print(self.__counter_title)
        print(self.__counter_date)



    def __str__(self):
        ret = "Number of tokens : {}\nFirst 20 tokens :\n{}".format(len(self.__tokens), self.__tokens[:20])
        return ret

    def set_of_terms(self):
        '''
        :return: a set of the tokens in the document
        '''
        return set(self.__tokens_neutral + self.__tokens_title + self.__tokens_date)

    def doc_id(self):
        '''
        here we use the fact that the first token is always the docid in the documents of our corpus
        :return: the docid of the document
        '''
        return self.__tokens_neutral[0]

    def term_frequecy(self, term):
        '''
        return the term-frequency of a term
        slide 8 : tf(t,d) = 1 + log(nt,d) or 0 if nt,d = 0
        :param term: the term for wich we seek the frequency
        :return: the term-frequency of the term
        '''
        return self.__counter_neutral[term.lower()] + self.__counter_title[term.lower()]*tw + self.__counter_date[term.lower()]*dw

        """exist = False
        term_fre = 1
        if term in (self.counter_neutral) :
            term_fre += log10(self.counter_neutral[term])
            exist = True
        if term in (self.counter_title) :
            term_fre +=  log10(self.counter_title[term] * tw)
            exist = True
        if term in (self.counter_date) :
            term_fre += log10(self.counter_date[term] * dw)
            exist = True
        if not exist :
            return 0

        return term_fre"""


