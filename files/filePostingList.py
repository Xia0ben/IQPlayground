from sortedcontainers import SortedDict

'''
PostingList class

author :Alexis Fossart
date :  08/10/2017

Class used to represent a posting list
'''


class FilePostingList:

    def __init__(self):
        self.ord_elems = list()
        self.rand_elems = SortedDict()

    def add_document(self, document_id, score):
        '''
        add a document and its score to the posting list
        allows 2 access :
            random access : use a dict for log time access
            ordered access : use a list
        :param document_id: the doc to add to the posting list
        :param score: the score of the doccument
        '''
        rank = 0
        for (doc_id, doc_score) in self.ord_elems:
            last_rank = rank
            if score <= doc_score:
                rank += 1
            if last_rank == rank:
                break

        self.ord_elems = self.ord_elems[:rank] + [(document_id, score)] + self.ord_elems[rank:(len(self.ord_elems))]
        self.rand_elems[document_id] = score

    def ordered_access(self):
        '''
        allows to access each elements of the list ordered by their score
        :return: a tuple (document_id, score)
        '''
        for elem in self.ord_elems:
            yield elem

    def document_score(self, document_id):
        '''
        return the score of a document in log time
        :param document_id: the document
        :return: the score of the document
        '''
        if document_id in self.rand_elems:
            return self.rand_elems[document_id]
        return 0

    def __len__(self):
        '''
        return the length of the posting list
        :return: the length of the posting list
        '''
        return len(self.ord_elems)