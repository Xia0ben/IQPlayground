from datetime import datetime
import itertools
from math import log10
import os

import numpy as np
from sortedcontainers import SortedDict

from files import PostingList, FileToPostingLists
from algorithm import VariableByte

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
                 documents,
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
        self.__time_start = datetime.now()

        self.__postinglist_file_path = "invertedfiles/{:%H%M%S}.plf".format(self.__time_start)

        __nb_tmp_inverted_file = 0

        tmp_inverted_file_base_path = "invertedfiles/tmp-{:%H%M%S}-".format(self.__time_start)

        doc_count = 0
        tmp_voc = SortedDict()
        tmp_path = "{}{}".format(tmp_inverted_file_base_path,
                                 __nb_tmp_inverted_file)
        tmp_files_path = []

        for document in documents:
            for term in document.set_of_terms():
                if term not in tmp_voc:
                    tmp_voc[term] = [0, PostingList()]
                tmp_voc[term][0] += 1
                id = document.doc_id()
                freq = document.term_frequecy(term)
                tmp_voc[term][1].add_document(id, freq)

            doc_count += 1

            if doc_count == memory_limit:
                doc_count = 0
                self._dump(tmp_path, tmp_voc)
                tmp_files_path.append(tmp_path)
                tmp_voc = SortedDict()
                __nb_tmp_inverted_file += 1
                tmp_path = "{}{}".format(tmp_inverted_file_base_path,
                                         __nb_tmp_inverted_file)

        self._dump(tmp_path, tmp_voc)
        tmp_files_path.append(tmp_path)

        tmp_files = []
        tmp_used = []
        for path in tmp_files_path:
            tmp_used.append(False)
            tmp_files.append(open(path, "r"))

        tmp_lines = []
        for file in tmp_files:
            tmp_lines.append(file.readline())

        self.vocabulary_of_term = SortedDict()
        self.term_random_access = SortedDict()

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

            term_rdm_access = [0,0,0,0,0,0]

            for i in min_lists:
                split = tmp_lines[i].split('\t')
                pl_string = "{}{}".format(pl_string, split[2].replace("\n", ","))
                tmp_used[i] = True

            freq = 0

            with open(self.__postinglist_file_path, "ab") as file:
                for val in pl_string.split(","):
                    if val != '':
                        freq += 1
                        if use_vbytes:
                            bytes_val = VariableByte.encoding_number(int(val))
                        else:
                            bytes_val = int(val).to_bytes(4, byteorder='big', signed=False)

                        pl_size += file.write(bytes_val)

            self.term_random_access[min_term] = term_rdm_access

            idf = log10(len(documents) / (1 + (freq/2)))

            self.vocabulary_of_term[min_term] = (offset, pl_size, idf)
            offset += pl_size

        for file in tmp_files:
            file.close()
        for file_path in tmp_files_path:
            os.remove(file_path)

        self.__postinglist_gen = FileToPostingLists(self.__postinglist_file_path, use_vbytes)

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
