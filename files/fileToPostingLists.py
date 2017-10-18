from math import log10

from files import PostingList

'''
PostingList class

author :Alexis Fossart
date :  08/10/2017

Class used to represent a posting list
'''


class FileToPostingLists:

    def __init__(self, pl_file):
        self.__pl_file = pl_file

    def gen_posting_list(self, offset, size, idf):
        posting_list = PostingList()
        pl_size = 0
        with open(self.__pl_file, "rb") as file:
            file.seek(offset)
            read = 0
            while read < size:
                pl_size += 1
                doc_id = int.from_bytes(file.read(4), byteorder='big')
                score = idf * (1 + log10(int.from_bytes(file.read(4), byteorder='big')))
                posting_list.add_document(doc_id, score)
                read += 4+4
        return posting_list, pl_size
