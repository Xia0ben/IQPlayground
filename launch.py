
from executable import Executable
from algorithm import NaiveAlgorithm, SimpleScanAlgorithm,  FA_Algorithm, TA_Algorithm
from stats import StatsControl as SC

ALGORITHMS_DESC = {
    "NAIVE": "A naive Top-K algorithm adding the scores of the documents",
    "SIMPLE": "A simple algorithm who select the documents where all the queried words appears",
    "FA": "Fagin's top-k query algorithm (FA)",
    "TA": "Fagin’s threshold algorithm (TA)"
}
DEFAULT_NUMBER_OF_RESULTS = 5
DEFAULT_ALGORITHM = "NAIVE"

file_path = "latimes/la100590"

exe = Executable()

algorithm = DEFAULT_ALGORITHM
number_of_results = DEFAULT_NUMBER_OF_RESULTS

if exe.inv_file is None:
    exe.indexing([file_path])

try:
    in_res = int(input("Number of results desired ? ").strip())
    number_of_results = in_res
except ValueError:
    print("Non-int value entered using default {}".format(DEFAULT_NUMBER_OF_RESULTS))

print("Algorithm description :")
for (name, desc) in ALGORITHMS_DESC.items():
    print("{}\t- {}".format(name, desc))

in_alg = input("Choose your algorithm : ").strip().upper()
if in_alg not in ALGORITHMS_DESC:
    algorithm = DEFAULT_ALGORITHM
    print("Non existing algorithm asked, using default : NAIVE")
else:
    algorithm = in_alg

while True:
    query = input("Query ? ")

    documents = exe.query(query, algorithm, 5)

    print("Your query is : {}".format(query))
    if documents is not None and len(documents) > 0:
        print("You may be interested by the following documents:")
        print("\t   score |\tdocument |\tfile_path")
        for doc in documents:
            print("\t{:8.5f} |\t{:8} |\t{}".format(doc[1], doc[0], doc[2]))
    else:
        print("Sorry no documents may be of interest to you. :(")

    print(SC.last_query())
