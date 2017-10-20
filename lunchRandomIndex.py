import os.path
import pickle

from files import InvertedFile, Reader
from algorithm import NaiveAlgorithm, SimpleScanAlgorithm
from algorithm import VectorsSimilarity

ALGORITHMS = {
    "NAIVE": NaiveAlgorithm,
    "SIMPLE": SimpleScanAlgorithm
}

ALGORITHMS_DESC = {
    "NAIVE": "A naive Top-K algorithm adding the scores of the documents",
    "SIMPLE": "A simple algorithm who select the documents where all the queried words appears"
}
DEFAULT_NUMBER_OF_RESULTS = 5
DEFAULT_ALGORITHM = ALGORITHMS["NAIVE"]

file_path = "latimes/la100590"
pickle_path = file_path.replace("latimes", "pickles")

# do we have a pickle file ?
if os.path.isfile(pickle_path):
    # yes we charge it
    with open(pickle_path, "rb") as file:
        inv_file = pickle.load(file)

else:
    # no we read the original file
    documents = Reader.read_file(file_path)

    print("Number of documents read : {}".format(len(documents)))

    inv_file = InvertedFile(documents)

    # we save the IF as a pickle file for next uses
    with open(pickle_path, "wb") as file:
        pickle.dump(inv_file, file)

dict_vectors_terms = inv_file.get_vectors_of_term()

#print(dict_vectors_terms.keys())

my_keys = dict_vectors_terms.keys()

print("Loaded Inverted File - {} terms found".format(len(inv_file.vocabulary_of_term)))

# for term in dict_vectors_terms.keys():

for choice_key in my_keys:
    choice_key_similarity = VectorsSimilarity.cosine_distances(dict_vectors_terms[choice_key], dict_vectors_terms)
    displayed_list = ["\"{}\" -> {}, ".format(a_, b_) for a_, b_ in zip(my_keys, choice_key_similarity)]
    print("|%s| : %s" % (choice_key, "".join(map(str, displayed_list))))

