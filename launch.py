from files import Reader

file_path = "latimes/la010189"

documents = Reader.read_file(file_path)

print("Number of documents read : {}".format(len(documents)))

for document in documents:
    print(document)
