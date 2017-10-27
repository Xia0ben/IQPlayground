from datetime import datetime
import itertools
from math import log10
import os

import numpy as np
from sortedcontainers import SortedDict

from files import PostingList, FileToPostingLists
from algorithm import VariableByte
from stats import StatsControl as SC
from algorithm import RandomIndex

'''
InvertedFile class

author :Alexis Fossart
date :  06/10/2017

Class used to represent an inverted file
'''


class InvertedFile:

    @staticmethod
    def _dump(path, voc):

        with open(path, "w") as tmp_file:
            for (term, [size, pl]) in voc.items():
                pl_str = ""
                for (doc_id, freq) in pl.alpha_access():
                    if pl_str != "":
                        pl_str = "{},{},{}".format(pl_str, doc_id, freq)
                    else:
                        pl_str = "{},{}".format(doc_id, freq)
                tmp_file.write("{}\t{}\t{}\n".format(term, size, pl_str))

    def __init__(self,
                 use_vbytes=True,
                 memory_limit= 50):
        '''
        Init an inverted file by creating a voc and the associated pl
        slide 6
        voc : vocabulary of terms
        pl : posting list
        an inverted file is a mapping between a vocabulary of terms and posting lists
        :param documents: a list of documents
        '''
        self.use_vbytes = use_vbytes
        self.memory_limit = memory_limit

        self.doc_id_vectors_list = dict()  # HERE

        self.__time_start = datetime.now()

        self.__postinglist_file_path = "invertedfiles/{:%H%M%S}.plf".format(self.__time_start)

        self.__nb_tmp_inverted_file = 0

        self.tmp_inverted_file_base_path = "invertedfiles/tmp-{:%H%M%S}-".format(self.__time_start)

        self.doc_count = 0
        self.tmp_voc = SortedDict()
        self.tmp_path = "{}{}".format(self.tmp_inverted_file_base_path,
                                      self.__nb_tmp_inverted_file)
        self.tmp_files_path = []
        self.nb_docs = 0


    def add_document(self, document):
        self.nb_docs += 1
        self.doc_id_vectors_list[document.doc_id()] = RandomIndex.get_random_index_vector() #HERE
        # print(self.doc_id_vectors_list[document.doc_id()])   #HERE
        for term in document.set_of_terms():
            if term not in self.tmp_voc:
                self.tmp_voc[term] = [0, PostingList()]
            self.tmp_voc[term][0] += 1
            id = document.doc_id()
            freq = document.term_frequecy(term)
            self.tmp_voc[term][1].add_document(id, freq)

        self.doc_count += 1

        if self.doc_count == self.memory_limit:
            self.doc_count = 0
            self._dump(self.tmp_path, self.tmp_voc)
            self.tmp_files_path.append(self.tmp_path)
            self.tmp_voc = SortedDict()
            self.__nb_tmp_inverted_file += 1
            self.tmp_path = "{}{}".format(self.tmp_inverted_file_base_path,
                                          self.__nb_tmp_inverted_file)

    def gen_pl_file(self):
        self._dump(self.tmp_path, self.tmp_voc)

        del self.tmp_voc

        self.tmp_files_path.append(self.tmp_path)

        tmp_files = []
        tmp_used = []
        for path in self.tmp_files_path:
            tmp_used.append(False)
            tmp_files.append(open(path, "r"))

        tmp_lines = []
        for file in tmp_files:
            tmp_lines.append(file.readline())

        self.vocabulary_of_term = SortedDict()
        self.vectors_of_term = SortedDict() #HERE

        offset = 0

        while True:

            min_term = ''
            min_lists = []
            for i in range(len(tmp_files)):
                if tmp_used[i] and tmp_lines[i] != '':
                    tmp_lines[i] = tmp_files[i].readline()
                    tmp_used[i] = tmp_lines[i] == ''

                if tmp_lines[i] != '':
                    term = tmp_lines[i].split('\t')[0]
                    if i == 0:
                        min_term = term
                    if term < min_term:
                        min_term = term
                        min_lists = [i]
                    elif term == min_term:
                        min_lists.append(i)

            if min_term == '':
                break

            pl_size = 0
            pl_string = ""

            for i in min_lists:
                split = tmp_lines[i].split('\t')
                pl_string = "{}{}".format(pl_string, split[2].replace("\n", ","))
                tmp_used[i] = True

            freq = 0

            term_rdm_index = [0] * RandomIndex.get_n()  # HERE

            with open(self.__postinglist_file_path, "ab") as file:
                if_doc_id = True  # HERE
                for val in pl_string.split(","):
                    if val != '':
                        if if_doc_id:  # HERE
                            term_rdm_index += self.doc_id_vectors_list[val] #HERE
                            term_rdm_index = list(map(lambda x, y: x + y, term_rdm_index,
                                                      self.doc_id_vectors_list[val]))  # HERE
                        freq += 1
                        if self.use_vbytes:
                            bytes_val = VariableByte.encoding_number(int(val))
                        else:
                            bytes_val = int(val).to_bytes(4, byteorder='big', signed=False)

                        pl_size += file.write(bytes_val)
                    if_doc_id = not if_doc_id  # HERE

            self.vectors_of_term[min_term] = term_rdm_index  # HERE
            # print(self.vectors_of_term[min_term])   # HERE
            # print()  # HERE

            idf = log10(self.nb_docs / (1 + (freq/2)))

            self.vocabulary_of_term[min_term] = (offset, pl_size, idf)
            offset += pl_size

        SC.last_indexing().add_pl_size(offset)

        for file in tmp_files:
            file.close()
        for file_path in self.tmp_files_path:
            os.remove(file_path)

        self.__postinglist_gen = FileToPostingLists(self.__postinglist_file_path, self.use_vbytes)

        # parallel read
        # combination
        # final PL

    def get_terms(self):
        return list([term for term in self.vocabulary_of_term.keys()])

    def get_documents(self, term):
        offset, pl_size, idf = self.vocabulary_of_term[term]
        # we create a list of generator witch yield their results
        posting_list, _ = self.__postinglist_gen.gen_posting_list(offset, pl_size, idf)
        for elem in posting_list.ordered_access():
            yield elem

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
        posting_lists = dict()
        sizes = dict()

        for term in terms:
            if term not in self.vocabulary_of_term:
                return

        for term in [term for term in terms if term in self.vocabulary_of_term]:
            ranks[term] = 0
            offset, pl_size, idf = self.vocabulary_of_term[term]
            # we create a list of generator witch yield their results
            posting_lists[term], sizes[term] = self.__postinglist_gen.gen_posting_list(offset, pl_size, idf)
            ordonated_accesses[term] = posting_lists[term].ordered_access()

        # while we have a term to explore we continue
        turn = len(ranks) > 0
        while turn:
            # we found the first term with the lowest rank
            term = next(filter(lambda x: ranks[x] == np.min(list(ranks.values())), ranks.keys()))
            ranks[term] += 1

            if ranks[term] <= sizes[term]:
                # we do the ordonated access to look for the document
                item = next(ordonated_accesses[term])
                if item[0] not in found_docs:
                    found_docs.append(item[0])
                    # we found a new doc, we send it
                    yield item
                    # for each other terms we send their score for the document
                    for other_term in [o_term for o_term in terms if o_term is not term]:
                        yield (item[0], posting_lists[other_term].document_score(item[0]))
            turn = np.any(list(map(lambda w: ranks[w] < sizes[w], ranks.keys())))

    def get_vectors_of_term(self):
        return self.vectors_of_term