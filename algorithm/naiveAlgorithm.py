import numpy as np
import heapq

from algorithm import BaseAlgorithm

'''
baseClass for an algorithm

author :Alexis Fossart
date :  08/10/2017

Abstract base class used to represent an algorithm
'''


class NaiveAlgorithm(BaseAlgorithm):

    @staticmethod
    def execute(query, inverted_file, number_of_results):
        '''
        we do a niave search in the corpus
        the score of each documents are added to create the final score for the search
        :param query: the query you want to look up
        :param inverted_file: the inverted file representing your corpus
        :param number_of_results: the desired number of results
        :return: the documents containing all of the terms in the query
        '''
        searched_terms = query.split()

        mapping_documents_scores = dict()

        # for each document returned by the parrallel scan we keep its score
        for (doc_id, score) in inverted_file.parallel_scan(searched_terms):
            if doc_id not in mapping_documents_scores:
                mapping_documents_scores[doc_id] = []
            mapping_documents_scores[doc_id].append(score)

        if len(mapping_documents_scores) == 0:
            return None

        results = []

        kept = []

        for(doc_id, scores) in mapping_documents_scores.items():
            if 0 not in scores:
                kept.append(doc_id)

        # for each document we push it and its score to a heapq
        for doc_id in kept:
            heapq.heappush(results, (np.sum(mapping_documents_scores[doc_id]), doc_id))

        # to use heapq we had to inverse doc_id and score in the tuples so we reverse them back during return
        return [(t[1], t[0]) for t in heapq.nlargest(number_of_results, results)]
