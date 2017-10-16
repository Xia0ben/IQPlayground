import os.path
import pickle

from files import InvertedFile, Reader
from algorithm import NaiveAlgorithm, SimpleScanAlgorithm

file_path = "latimes/la100590"

documents = Reader.read_file(file_path)

print("Number of documents read : {}".format(len(documents)))

inv_file = InvertedFile(documents)
