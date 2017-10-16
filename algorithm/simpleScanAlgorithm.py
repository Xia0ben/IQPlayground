import itertools

from algorithm import BaseAlgorithm

'''
baseClass for an algorithm

author :Alexis Fossart
date :  08/10/2017

Abstract base class used to represent an algorithm
'''


class SimpleScanAlgorithm(BaseAlgorithm):

    @staticmethod
    def execute(query, inverted_file, number_of_results):
        '''
        Execute a simple scan of the corpus :
        we return each document that contain each term of the query
        the score is set to 1 if all the terms are in the document
        :param query: the query you want to look up
        :param inverted_file: the inverted file representing your corpus
        :param number_of_results: the desired number of results
        :return: the documents containing all of the terms in the query
        '''
        searched_terms = query.split()

        mapping_term_documents = dict()

        for term in searched_terms:
            mapping_term_documents[term] = list()
            if term in inverted_file.vocabulary_of_term:
                # We access the VOC and add all documents found in the term's posting list to a set
                for (doc_id, score) in inverted_file.get_documents(term):
                    mapping_term_documents[term].append(tuple((doc_id, 1)))

        if len(mapping_term_documents) == 0:
            return None

        # We init the results with the set of docs from the first term
        results = set(next(iter(mapping_term_documents.values())))

        for (term, documents) in mapping_term_documents.items():
            # We do the intersection of the documents found for each term
            results.intersection_update(documents)

        if len(results) > number_of_results:
            # if we found more doc than required we return the 5 first found
            return itertools.islice(list(results), number_of_results)

        return results
