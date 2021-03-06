from collections import Counter
from math import log10
import re, string

from nltk.corpus import stopwords
from nltk import word_tokenize
from files import stemmer
'''
Document class

author :Alexis Fossart
date :  06/10/2017

Class used to represent a document in memory
'''


class Document:

    def __init__(self,
                 xml_text,
                 ignore_case=True,
                 ignore_stop_words=True,
                 stemming=True,
                 use_weights=True,
                 title_weight=5,
                 date_weight=2):
        """
        Init of the document
        :param xml_text: xml text representing the document
        :param ignore_case: should we convert the xml to lower case ?
        :param ignore_stop_words: shoul we ignore stop words ?
        :param stemming: should we stemm ?
        :param use_weights: should we use weights ?
        :param title_weight: weight for title
        :param date_weight: weight for date
        """

        self.__title_weight = 1
        self.__date_weight = 1

        if use_weights:
            text = xml_text
            self.__title_weight = title_weight
            self.__date_weight = date_weight
        else:
            text = re.sub("<[^>]*>", "", xml_text)

        if ignore_case:
            text = text.lower()

        self.__tokens_title = []
        self.__tokens_date = []
        self.__tokens_neutral = []

        type_t = ""

        # Tokenization
        for token in text.split():
            if token.lower() == "<title>":
                type_t = "title"
            elif token.lower() == "<date>":
                type_t = "date"
            elif token.lower() == "</title>" or token.lower() == "</date>":
                type_t = ""
            else:
                t_token = token.translate(str.maketrans('','',string.punctuation))
                if len(t_token) > 0:
                    if type_t == "title":
                        self.__tokens_title.append(t_token)
                    elif type_t == "date":
                        self.__tokens_date.append(t_token)
                    else:
                        if token.lower()[0] != "<" and token.lower()[-1] != ">":
                            self.__tokens_neutral.append(t_token)

        if ignore_stop_words:
            cached_stop_words = stopwords.words("english")
            punctuations = list(string.punctuation)
            self.__tokens_title = [token for token in self.__tokens_title
                                   if token not in cached_stop_words
                                   and token not in punctuations]
            self.__tokens_date = [token for token in self.__tokens_date
                                  if token not in cached_stop_words
                                  and token not in punctuations]
            self.__tokens_neutral = [token for token in self.__tokens_neutral
                                     if token not in cached_stop_words
                                     and token not in punctuations]

        if stemming:
            sm = stemmer.Stemmer()
            for i in range(len(self.__tokens_title)):
                self.__tokens_title[i] = sm.stem(self.__tokens_title[i], 0, len(self.__tokens_title[i]) - 1)
            for i in range(len(self.__tokens_date)):
                self.__tokens_date[i] = sm.stem(self.__tokens_date[i], 0, len(self.__tokens_date[i]) - 1)
            for i in range(len(self.__tokens_neutral)):
                self.__tokens_neutral[i] = sm.stem(self.__tokens_neutral[i], 0, len(self.__tokens_neutral[i]) - 1)

        self.__counter_neutral = Counter(self.__tokens_neutral)
        self.__counter_title = Counter(self.__tokens_title)
        self.__counter_date = Counter(self.__tokens_date)

    def set_of_terms(self):
        '''
        :return: a set of the tokens in the document
        '''
        res = set(self.__tokens_neutral)
        res.update(self.__tokens_title)
        res.update(self.__tokens_date)
        return res

    def doc_id(self):
        '''
        here we use the fact that the first token is always the docid in the documents of our corpus
        :return: the docid of the document
        '''
        return self.__tokens_neutral[1]

    def term_frequecy(self, term):
        '''
        return the frequency of a term in the document
        :param term: the term for wich we seek the frequency
        :return: the term-frequency of the term
        '''
        return (self.__counter_neutral[term]
                + self.__counter_title[term] * self.__title_weight
                + self.__counter_date[term] * self.__date_weight)
