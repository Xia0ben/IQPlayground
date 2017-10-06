from files import Document

'''
Reading class

author :Alexis Fossart
date :  06/10/2017

Class used to read document files from the disk
'''

class Reader:

    @staticmethod
    def read_file(file_path):
        '''
        Read a file and return it as an array of documents
        :param file_path: path to the read file
        :return: an array of Documents
        '''
        documents = []

        with open(file_path) as file:
            document_string = ""
            for line in file:
                document_string = "{}\n{}".format(document_string, line)

                if "</DOC>" in line:
                    documents.append(Document(document_string))
                    document_string = ""

        return documents