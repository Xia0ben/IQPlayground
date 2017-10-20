from datetime import datetime


'''
Stats class

author :Alexis Fossart
date :  08/10/2017

Class used to represent the stats of an indexing job
'''


class IndexingStats:

    def __init__(self):
        self.start_time = datetime.now()
        self.finish_time = None
        self.file_size = 0

    def stop(self):
        if self.finish_time is None:
            self.finish_time = datetime.now()
        else:
            raise ArithmeticError()

    def add_pl_size(self, size_of_pl):
        if self.finish_time is None:
            self.file_size = size_of_pl

    def log(self,
            files,
            ignore_case=True,
            ignore_stop_words=True,
            stemming=True,
            use_weights=True,
            title_weight=5,
            date_weight=2,
            memory_limit=50,
            use_vbytes=True):
        log_str = """
Indexing configuration:
    Number of files : {}
    Ignore case : {}
    Ignore stop words : {}
    Stemming : {}
    Use of weight : {}
    Title weight : {}
    Date weight : {}
    Use of variable bytes : {}
    Memory limit : {}
{}
""".format(len(files),
           ignore_case,
           ignore_stop_words,
           stemming,
           use_weights,
           title_weight,
           date_weight,
           use_vbytes,
           memory_limit,
           self.__str__())
        with open("indexing.logs", "a") as file:
            file.write(log_str)

    def __str__(self):
        if self.finish_time is None:
            tot_time = datetime.now() - self.start_time
        else:
            tot_time = self.finish_time - self.start_time

        end_time = self.finish_time
        end_time_params = "%H:%M:%S.%f"
        if end_time is None:
            end_time = "Not yet finished"
            end_time_params = ""

        values = {
            "start_time": self.start_time,
            "file_size": self.file_size,
            "exec_time": tot_time,
            "end_time": end_time,
            "end_time_params": end_time_params
        }
        res ="""
Stats for indexing :
    Started at : {start_time:%H:%M:%S.%f}
    Ended at : {end_time:{end_time_params}}
    Execution time : {exec_time}
    Size of the pl file generated : {file_size}
""".format(**values)
        return res
