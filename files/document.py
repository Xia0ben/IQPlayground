import re

from nltk import word_tokenize

'''
Document class

author :Alexis Fossart
date :  06/10/2017

Class used to represent a document in memory
'''


class Document:
    def __init__(self, xml_text):
        text = re.sub("<[^>]*>", "", xml_text)
        self.__tokens = word_tokenize(text)

    def __str__(self):
        ret = "Number of tokens : {}\nFirst 20 tokens :\n{}".format(len(self.__tokens), self.__tokens[:20])
        return ret
