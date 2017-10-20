from datetime import datetime

from sortedcontainers import SortedDict

from stats import QueryStats

'''
StatsControl class

author :Alexis Fossart
date :  08/10/2017

Class used to generate and control stats over the project
'''


class StatsControl:

    queries = []
    last = None

    @classmethod
    def new_query(cls, query):
        start = datetime.now()
        cls.queries.append(QueryStats(query))

    @classmethod
    def last_query(cls):
        if len(cls.queries) > 0:
            return cls.queries[-1]
        return None

    @classmethod
    def all_queries(cls):
        for stats in cls.queries:
            yield stats