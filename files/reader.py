from files import Document

'''
Reading class

author :Alexis Fossart
date :  06/10/2017

Class used to read document files from the disk
'''

class Reader:

    @staticmethod
    def read_file(file_path,
                 ignore_case=True,
                 ignore_stop_words=True,
                 stemming=True,
                 use_weights=True,
                 title_weight=5,
                 date_weight=2):
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
                    documents.append(Document(document_string,
                                              ignore_case,
                                              ignore_stop_words,
                                              stemming,
                                              use_weights,
                                              title_weight,
                                              date_weight))
                    document_string = ""

        return documents