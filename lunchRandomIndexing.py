import os.path
import pickle
import operator

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


print("Loaded Inverted File - {} terms found".format(len(inv_file.vocabulary_of_term)))

'''
Begin executing the random index algorithm
'''

# Get the terms vectors :
dict_vectors_terms = inv_file.get_vectors_of_term()

# Get the list of terms :
my_keys = dict_vectors_terms.keys()

# The list of terms to choose one :
print(my_keys)

# The chosen term :
choice_key = input("\nYour word choice ? ")

# Choose the number of top displayed similarity results :
top_results = int(input("number of similar words in display ? "))


# Calculate distance when the term exist in our vocabulary :
if choice_key in dict_vectors_terms:

    choice_key_similarity = VectorsSimilarity.cosine_distances(dict_vectors_terms[choice_key], dict_vectors_terms)

    # displayed_list = ["\"{}\" -> {}, ".format(a_, b_) for a_, b_ in zip(my_keys, choice_key_similarity)]

    titles = sorted(choice_key_similarity, key=choice_key_similarity.get)
    values = sorted(choice_key_similarity.values())

    # print(sorted(choice_key_similarity, key=choice_key_similarity.get))
    # print(sorted(choice_key_similarity.values()))
    # print(sorted(choice_key_similarity.items(), key=operator.itemgetter(0)))

    print("\n *********** Similarity of -> %s : *********** " % choice_key)

    del titles[0]

    del values[0]

    displayed_list = ["{} : {}".format(a_, b_) for a_, b_ in zip(titles[:top_results], values[:top_results])]

    print(displayed_list)

else:
    print("\nWord not exist !")


