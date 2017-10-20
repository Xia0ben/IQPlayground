import os.path
import pickle

from files import InvertedFile, Reader
from algorithm import NaiveAlgorithm, SimpleScanAlgorithm,  FA_Algorithm
from stats import StatsControl as SC

ALGORITHMS = {
    "NAIVE": NaiveAlgorithm,
    "SIMPLE": SimpleScanAlgorithm,
    "FA": FA_Algorithm
}

ALGORITHMS_DESC = {
    "NAIVE": "A naive Top-K algorithm adding the scores of the documents",
    "SIMPLE": "A simple algorithm who select the documents where all the queried words appears",
    "FA": "Fagin's top-k query algorithm (FA)"
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

algorithm = DEFAULT_ALGORITHM
number_of_results = DEFAULT_NUMBER_OF_RESULTS

try:
    in_res = int(input("Number of results desired ? ").strip())
    number_of_results = in_res
except ValueError:
    print("Non-int value entered using default {}".format(DEFAULT_NUMBER_OF_RESULTS))

print("Algorithm description :")
for (name, desc) in ALGORITHMS_DESC.items():
    print("{}\t- {}".format(name, desc))
try:
    in_alg = ALGORITHMS[input("Choose your algorithm : ").strip().upper()]
    algorithm = in_alg
except KeyError:
    print("Non existing algorithm asked, using default : NAIVE")

algorithm = algorithm()

while True:
    query = input("Query ? ")

    SC.new_query(query)

    documents = algorithm.execute(query, inv_file, number_of_results)

    SC.last_query().stop()

    print("Your query is : {}".format(query))
    if documents is not None and len(documents) > 0:
        print("You may be interested by the following documents:")
        print("\t   score |\tdocument")
        for doc in documents:
            print("\t{:8.5f} |\t{}".format(doc[1], doc[0]))
    else:
        print("Sorry no documents may be of interest to you. :(")

    print(SC.last_query())
