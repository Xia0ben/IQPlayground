from abc import ABC, abstractmethod

'''
baseClass for an algorithm

author :Alexis Fossart
date :  08/10/2017

Abstract base class used to represent an algorithm
'''


class BaseAlgorithm(ABC):

    @staticmethod
    @abstractmethod
    def execute(query, inverted_file, number_of_results):
        '''
        Execute an algorithm to look up a query in your corpus
        :param query: the query you want to look up
        :param inverted_file: the inverted file representing your corpus
        :param number_of_results: the desired number of results
        :return: the results as a list of tuples (document_id, score) ordonated by their score
        '''
        pass
