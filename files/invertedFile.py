from datetime import datetime
import itertools
from math import log10
import os

import numpy as np
from sortedcontainers import SortedDict

from files import PostingList, FilePostingList

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

    def __init__(self, documents, memory_limit= 50):
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
                pl_size += int(split[1])
                pl_string = "{}{}".format(pl_string, split[2].replace("\n", ","))
                tmp_used[i] = True

            self.vocabulary_of_term[min_term] = (offset, pl_size)
            offset += pl_size

            with open(self.__postinglist_file_path, "ab") as file:
                for val in pl_string.split(","):
                    if val != '':
                        file.write(int(val).to_bytes(4, byteorder='big', signed=False))


        # parallel read
        # combination
        # final PL

    def __old_init__(self, documents):

        self.vocabulary_of_term = SortedDict()

        terms = set()
        for document in documents:
            terms.update(document.set_of_terms())

        for term in terms:
            frequency = 0
            tf_dict = dict()

            for document in documents:
                # Calc of the term frequency in each document
                # Slide 8
                term_frequency = document.term_frequecy(term)
                if term_frequency > 0:
                    frequency += 1
                    tf_dict[document.doc_id()] = term_frequency

            # Calc of the idf of the term
            # Slide 9 & 10
            idf = log10(len(documents) / (1 + frequency))

            posting_list = PostingList()

            for document_id in tf_dict:
                # Calc of the score for each document and add it to the posting list
                # Slide 11
                posting_list.add_document(document_id, tf_dict[document_id] * idf)

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
            ordonated_accesses[term] = self.vocabulary_of_term[term]['posting_list'].ordered_access()

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