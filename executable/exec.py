import os.path
import pickle

from sortedcontainers import SortedDict

from files import InvertedFile, Reader
from algorithm import NaiveAlgorithm, SimpleScanAlgorithm, FA_Algorithm, TA_Algorithm
from stats import StatsControl as SC

'''
Executable class

author :Alexis Fossart
date :  20/10/2017

Allow the use of the different methods
and algorithms to index and query files
'''


class Exec:
    ALGORITHMS = {
        "NAIVE": NaiveAlgorithm,
        "SIMPLE": SimpleScanAlgorithm,
        "FA": FA_Algorithm,
        "TA": TA_Algorithm
    }

    ALGORITHMS_DESC = {
        "NAIVE": "A naive Top-K algorithm adding the scores of the documents",
        "SIMPLE": "A simple algorithm who select the documents where all the queried words appears",
        "FA": "Fagin's top-k query algorithm (FA)",
        "TA": "Fagin’s threshold algorithm (TA)"
    }

    DEFAULT_NUMBER_OF_RESULTS = 5
    DEFAULT_ALGORITHM = "NAIVE"

    PICKLES = ["pickles/if.pkl", "pickles/ids.pkl"]

    def __init__(self):
        try:
            os.stat("pickles")
        except:
            os.mkdir("pickles")

        try:
            os.stat("invertedfiles")
        except:
            os.mkdir("invertedfiles")

        if os.path.isfile(self.PICKLES[0]):
            with open(self.PICKLES[0], "rb") as file:
                self.inv_file = pickle.load(file)
            with open(self.PICKLES[1], "rb") as file:
                self.__id_to_filename = pickle.load(file)
                self.current_status = "Pickle file loaded - You can query"
        else:
            self.inv_file = None
            self.__id_to_filename = SortedDict()
            self.current_status = "Waiting to index files"

    def indexing(self,
                 files,
                 ignore_case=True,
                 ignore_stop_words=True,
                 stemming=True,
                 use_weights=True,
                 title_weight=5,
                 date_weight=2,
                 memory_limit=50,
                 use_vbytes=True):

        documents = []

        self.current_status = "Indexing - Starting"

        for file in files:
            self.current_status = "Indexing - {}".format(file)
            file_docs = Reader.read_file(file,
                                         ignore_case,
                                         ignore_stop_words,
                                         stemming,
                                         use_weights,
                                         title_weight,
                                         date_weight)
            for doc in file_docs:
                self.__id_to_filename[int(doc.doc_id())] = file
            documents.extend(file_docs)

        self.current_status = "Indexing - Making the inverted file"

        self.inv_file = InvertedFile(documents,
                                     use_vbytes,
                                     memory_limit)

        self.current_status = "Indexing - Saving to pickle file"

        with open(self.PICKLES[0], "wb") as file:
            pickle.dump(self.inv_file, file)
        with open(self.PICKLES[1], "wb") as file:
            pickle.dump(self.__id_to_filename, file)

        self.current_status = "Indexing - Finished - You can query"

    def query(self, query="", algorithm="NAIVE", number_of_results=5):
        SC.new_query(query)
        self.current_status = "Querying - Using {} alogrithm".format(algorithm)
        documents = self.ALGORITHMS[algorithm]().execute(query,
                                                         self.inv_file,
                                                         number_of_results)
        SC.last_query().stop()


        results = []

        for document in documents:
            results.append([document[0],document[1],self.__id_to_filename[document[0]]])

        self.current_status = "Querying - Finished"

        return results
