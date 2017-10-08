import itertools
from math import log10

import numpy as np

from files import PostingList

'''
InvertedFile class

author :Alexis Fossart
date :  06/10/2017

Class used to represent an inverted file
'''


class InvertedFile:

    def __init__(self, documents):
        '''
        Init an inverted file by creating a voc and the associated pl
        slide 6
        voc : vocabulary of terms
        pl : posting list
        an inverted file is a mapping between a vocabulary of terms and posting lists
        :param documents: a list of documents
        '''
        terms = set()
        for document in documents:
            terms.update(document.set_of_terms())

        self.vocabulary_of_term = dict()

        for term in terms:
            frequency = 0
            tf_list = dict()

            for document in documents:
                # Calc of the term frequency in each document
                # Slide 8
                term_frequency = document.term_frequecy(term)
                if term_frequency > 0:
                    frequency += 1
                    tf_list[document.doc_id()] = term_frequency

            # Calc of the idf of the term
            # Slide 9 & 10
            idf = log10(len(documents) / (1 + frequency))

            posting_list = PostingList()

            for document_id in tf_list:
                # Calc of the score for each document and add it to the posting list
                # Slide 11
                posting_list.add_document(document_id, tf_list[document_id] * idf)

            self.vocabulary_of_term[term] = {'size': len(posting_list),
                                             'posting_list': posting_list}

    def parallel_scan(self, terms):
        '''
        do the parallel scan of the inverted file
        is a generator witch returns a doc and its score at each call
        first find a doc in the current term PL
        then find the doc in all other terms' PL
        and then go to the next term
        if the next doc is already found skip it and go to the next term
        :param terms: terms used in the scan
        '''

        found_docs = []
        ranks = dict()
        ordonated_accesses = dict()
        for term in [term for term in terms if term in self.vocabulary_of_term]:
            ranks[term] = 0
            # we create a list of generator witch yield their results
            ordonated_accesses[term] = self.vocabulary_of_term[term]['posting_list'].ordonated_access()

        # while we have a term to explore we continue
        turn = len(ranks) > 0
        while turn:
            # we found the first term with the lowest rank
            term = next(filter(lambda x: ranks[x] == np.min(list(ranks.values())), ranks.keys()))
            ranks[term] += 1

            if ranks[term] <= self.vocabulary_of_term[term]['size']:
                # we do the ordonated access to look for the document
                item = next(ordonated_accesses[term])
                if item[0] not in found_docs:
                    found_docs.append(item[0])
                    # we found a new doc, we send it
                    yield item
                    # for each other terms we send their score for the document
                    for other_term in [o_term for o_term in terms if o_term is not term]:
                        yield (item[0], self.vocabulary_of_term[term]['posting_list'].document_score(item[0]))
            turn = np.any(list(map(lambda w: ranks[w] < self.vocabulary_of_term[w]['size'], ranks.keys())))