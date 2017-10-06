import os.path
import pickle

from files import Inverted_File, Reader

file_path = "latimes/la051090"
pickle_path = "pickles/la051090"

if os.path.isfile(pickle_path):
    with open(pickle_path, "rb") as file:
        inv_file = pickle.load(file)
else:
    documents = Reader.read_file(file_path)

    print("Number of documents read : {}".format(len(documents)))

    inv_file = Inverted_File(documents)

    with open(pickle_path, "wb") as file:
        pickle.dump(inv_file, file)

for term in inv_file.vocabulary_of_term:
    print("{} - size : {}".format(term, inv_file.vocabulary_of_term[term]['size']))
