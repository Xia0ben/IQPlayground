import numpy as np
import heapq

from numpy.distutils.system_info import numarray_info

from algorithm import BaseAlgorithm

'''
baseClass for an algorithm

author :Belgharib Zakaria
date :  18/10/2017

Abstract base class used to represent an algorithm
'''


class TA_Algorithm(BaseAlgorithm):

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
        k = number_of_results

        U_min = 999999999
        C = {}
        temp = {}

        for (doc_id, score) in inverted_file.parallel_scan(searched_terms):

            if len(temp) < k :
                if doc_id in temp :
                    temp[doc_id] = [(temp[doc_id][0] + score), (temp[doc_id][1] + 1)]
                else :
                    temp[doc_id] = [score, 1]
                if temp[doc_id][1] == nbre_terms :
                        C[doc_id] = temp[doc_id][0] / nbre_terms
                        if C[doc_id] < U_min:
                            U_min = C[doc_id]
            """else :
                if doc_id in temp :
                    temp[doc_id] = [(temp[doc_id][0] + score), (temp[doc_id][1] + 1)]
                else :
                    temp[doc_id] = [score, 1]
                if temp[doc_id][1] == nbre_terms :
                        temp[doc_id][0] = temp[doc_id][0] / nbre_terms
                        if temp[doc_id][0] > U_min:
                            kk=0
                            for k, v in C.items() :
                                if v == U_min:
                                    kk=k
                                    print(kk)
                            del C[kk]
                            C[doc_id] = temp[doc_id][0]
                            U_min = min(C)
                            print(doc_id)"""

        T = [[k, v] for k, v in C.items()]
        return T







