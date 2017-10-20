from math import log10

from algorithm import VariableByte
from files import PostingList
from stats import StatsControl as SC

'''
FileToPostingLists class

author :Alexis Fossart
date :  08/10/2017

Class used to read pl from file
'''


class FileToPostingLists:

    def __init__(self, pl_file, use_vbytes=True):
        self.__pl_file = pl_file
        self.__use_vbytes = use_vbytes

    def gen_posting_list(self, offset, size, idf):
        posting_list = PostingList()
        pl_size = 0
        with open(self.__pl_file, "rb") as file:
            SC.last_query().add_mem_access()
            file.seek(offset)
            if self.__use_vbytes:
                bytes_read = file.read(size)
                numbers = VariableByte.decoding(bytes_read)
                for i in range(0, len(numbers), 2):
                    doc_id = numbers[i]
                    score = idf * (1 + log10(numbers[i + 1]))
                    posting_list.add_document(doc_id, score)
                    pl_size += 1
            else:
                read = 0
                while read < size:
                    pl_size += 1
                    doc_id = int.from_bytes(file.read(4), byteorder='big')
                    score = idf * (1 + log10(int.from_bytes(file.read(4), byteorder='big')))
                    posting_list.add_document(doc_id, score)
                    read += 4+4
        return posting_list, pl_size
