from math import log10

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

