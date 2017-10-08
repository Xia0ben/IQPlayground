import os.path
import pickle

from files import InvertedFile, Reader
from algorithm import  SimpleScanAlgorithm

file_path = "latimes/la100590"
pickle_path = "pickles/la100590"

if os.path.isfile(pickle_path):
    with open(pickle_path, "rb") as file:
        inv_file = pickle.load(file)

else:
    documents = Reader.read_file(file_path)

    print("Number of documents read : {}".format(len(documents)))

    inv_file = InvertedFile(documents)

    with open(pickle_path, "wb") as file:
        pickle.dump(inv_file, file)

print("Loaded Inverted File - {} terms found".format(len(inv_file.vocabulary_of_term)))

algorithm = SimpleScanAlgorithm()

while True:
    query = input("Query ? ")
    print("Your query is : {}".format(query))
    documents = algorithm.execute(query, inv_file, 5)
    if documents is not None:
        print("You may be interested by the following documents:")
        print("\tscore\t |\tdocument")
        for doc in documents:
            print("\t{:8.5f} | {}".format(doc[1], doc[0]))
    else:
        print("Sorry no documents may be of interest to you. :(")
