from math import log10

class Inverted_File:

    def __init__(self, documents):
        terms = set()
        for document in documents:
            terms.update(document.set_of_terms())

        self.vocabulary_of_term = dict()

        for term in terms:
            frequency = 0
            posting_list = dict()

            for document in documents:
                term_frequency = document.term_frequecy(term)
                if term_frequency > 0:
                    frequency += 1
                    posting_list[document.doc_id()] = term_frequency

            idf = log10( len(documents) / (1 + frequency))

            for document_id in posting_list:
                posting_list[document_id] *= idf

            self.vocabulary_of_term[term] = {'size': len(posting_list),
                                             'posting_list': posting_list}
