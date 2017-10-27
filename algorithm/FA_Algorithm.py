import numpy as np
import heapq

from numpy.distutils.system_info import numarray_info

from algorithm import BaseAlgorithm

'''
baseClass for an algorithm

author :Belgharib Zakaria
date :  16/10/2017

Abstract base class used to represent an algorithm
'''


class FA_Algorithm(BaseAlgorithm):

    @staticmethod
    def execute(query, inverted_file, number_of_results):
        '''
        :param query: the query you want to look up
        :param inverted_file: the inverted file representing your corpus
        :param number_of_results: the desired number of results
        :return: the documents containing all of the terms in the query
        '''
        searched_terms = query.split()
        nbre_terms = len(searched_terms)

        M = {}
        C = []

        for (doc_id, score) in inverted_file.parallel_scan(searched_terms):
            if doc_id in M:

                M[doc_id] = [(M[doc_id][0] + score), (M[doc_id][1]+1)]

                if M[doc_id][1] == nbre_terms :
                    C.append((doc_id, (M[doc_id][0]+score)/M[doc_id][1]+1))
                    M.__delitem__(doc_id)
                    if len(C) == number_of_results:
                        return sorted(C)

            else:
                M[doc_id] = [score, 1]
                if nbre_terms == 1:
                    if len(M) == number_of_results:
                        C = [[k, v[0]] for k, v in M.items()]
                        return sorted(C)


        return C







