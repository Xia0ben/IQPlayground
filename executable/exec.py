import os.path
import pickle
from datetime import datetime


from sortedcontainers import SortedDict

from files import InvertedFile, Reader
from algorithm import NaiveAlgorithm, FA_Algorithm, TA_Algorithm
from stats import StatsControl as SC

from randomindexing import VectorsSimilarity


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
        "FA": FA_Algorithm,
        "TA": TA_Algorithm
    }

    ALGORITHMS_DESC = {
        "NAIVE": "A naive Top-K algorithm adding the scores of the documents",
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
        """
        Launch the indexing of a list of files
        :param files: the paths to the files to index
        :param ignore_case: should case be ignored in the indexing ?
        :param ignore_stop_words: should stop words be ignored ?
        :param stemming: should we stemm the tokens ?
        :param use_weights: shoud we differenciate word with their position in the document ?
        :param title_weight: weight for words in title
        :param date_weight: weight for words in the date
        :param memory_limit: limit on the memory before a flush in a temp file
        :param use_vbytes: usage of variable bytes for the final posting list ?
        :return: when the indexing is finished
        """

        SC.new_indexing()

        documents = []

        self.current_status = "Indexing - Starting"

        self.__id_to_filename = SortedDict()

        self.inv_file = InvertedFile(use_vbytes,
                                     memory_limit)
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
                self.inv_file.add_document(doc)


        self.current_status = "Indexing - Making the inverted file"

        self.inv_file.gen_pl_file()

        self.current_status = "Indexing - Saving to pickle file"

        with open(self.PICKLES[0], "wb") as file:
            pickle.dump(self.inv_file, file)
        with open(self.PICKLES[1], "wb") as file:
            pickle.dump(self.__id_to_filename, file)

        self.current_status = "Indexing - Finished - You can query"

        SC.last_indexing().stop()
        SC.last_indexing().log(
                 files,
                 ignore_case,
                 ignore_stop_words,
                 stemming,
                 use_weights,
                 title_weight,
                 date_weight,
                 memory_limit,
                 use_vbytes)


    def query(self,
              query="",
              algorithm="NAIVE",
              number_of_results=5):
        """
        Query the inverted file for documents
        :param query: the query
        :param algorithm: the name fo the algorithm to use (a key in ALGORITHM)
        :param number_of_results: the number of results expected
        :return: an array of array containing [doc_id, score, path to the file containing the documents]
        """
        SC.new_query(query)

        self.current_status = "Querying - Using {} alogrithm".format(algorithm)
        documents = self.ALGORITHMS[algorithm]().execute(query,
                                                         self.inv_file,
                                                         number_of_results)
        SC.last_query().stop()
        if documents is not None:
            SC.last_query().log(algorithm,
                                number_of_results,
                                len(documents))
        else:
            SC.last_query().log(algorithm,
                                number_of_results,
                                0)


        results = []

        if documents is not None:
            for document in documents:
                results.append([document[0],document[1],self.__id_to_filename[document[0]]])

        self.current_status = "Querying - Finished"

        return results

    '''
    random_indexing:
        params:
            choice_key  : (string) which is the term
            top_results : (int) the number of top results
        result:
            a list of tuples, which a tuple contain in first the term, and second the distance
    '''
    def random_indexing(self, choice_key, top_results):

        # Get the terms vectors :
        dict_vectors_terms = self.inv_file.get_vectors_of_term()

        # Calculate distance when the term exist in our vocabulary :
        if choice_key in dict_vectors_terms:

            choice_key_similarity = VectorsSimilarity.cosine_distances(dict_vectors_terms[choice_key],
                                                                       dict_vectors_terms)

            titles = sorted(choice_key_similarity, key=choice_key_similarity.get)
            values = sorted(choice_key_similarity.values())

            del titles[0]
            del values[0]

            titles_top = titles[:top_results]
            values_top = values[:top_results]

            final_results = [0] * top_results

            for i in range(top_results):
                final_results[i] = (titles_top[i], values_top[i])

            return final_results
