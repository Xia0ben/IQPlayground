from datetime import datetime

from sortedcontainers import SortedDict

from stats import QueryStats, IndexingStats

'''
StatsControl class

author :Alexis Fossart
date :  08/10/2017

Class used to generate and control stats over the project
'''


class StatsControl:

    indexings = []
    queries = []

    @classmethod
    def new_indexing(cls):
        cls.indexings.append(IndexingStats())

    @classmethod
    def new_query(cls, query):
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

    @classmethod
    def last_indexing(cls):
        if len(cls.indexings) > 0:
            return cls.indexings[-1]
        return None

    @classmethod
    def all_indexings(cls):
        for stats in cls.indexings:
            yield stats