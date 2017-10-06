import os.path
import pickle

from files import Inverted_File, Reader

file_path = "latimes/la100590"
pickle_path = "pickles/la100590"

if os.path.isfile(pickle_path):
    with open(pickle_path, "rb") as file:
        inv_file = pickle.load(file)

else:
    documents = Reader.read_file(file_path)

    print("Number of documents read : {}".format(len(documents)))

    inv_file = Inverted_File(documents)

    with open(pickle_path, "wb") as file:
        pickle.dump(inv_file, file)

print("Loaded Inverted File - {} terms found".format(len(inv_file.vocabulary_of_term)))

while True:
    query = input("Query ? ")
    print("Your query is : {}".format(query))
    documents = inv_file.scan(query)
    if documents is not None:
        print("You may be interested by the folowing documents:")
        for doc in documents:
            print("\t - {}".format(doc))
    else:
        print("Sorry no documents may be of interest to you. :(")
