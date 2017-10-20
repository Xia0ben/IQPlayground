from datetime import datetime


'''
Stats class

author :Alexis Fossart
date :  08/10/2017

Class used to represent the stats of a query
'''

class QueryStats:

    def __init__(self, query):
        self.query = query
        self.start_time = datetime.now()
        self.pl_accesses = 0
        self.finish_time = None
        self.memory_accesses = 0
        self.total_time = self.start_time

    def stop(self):
        if self.finish_time is None:
            self.finish_time = datetime.now()
            self.total_time = self.finish_time - self.start_time
        else:
            raise ArithmeticError()

    def add_mem_access(self):
        if self.finish_time is None:
            self.memory_accesses += 1

    def add_pl_access(self):
        if self.finish_time is None:
            self.pl_accesses += 1

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
            "query": self.query,
            "start_time": self.start_time,
            "mem_access": self.memory_accesses,
            "if_access": self.pl_accesses,
            "exec_time": tot_time,
            "end_time": end_time,
            "end_time_params": end_time_params
        }
        res ="""
Stats for query : {query}
    Started at : {start_time:%H:%M:%S.%f}
    Ended at : {end_time:{end_time_params}}
    Execution time : {exec_time}
    Number of access to the disk : {mem_access}
    Number of access to the inverted file : {if_access}
""".format(**values)
        return res
