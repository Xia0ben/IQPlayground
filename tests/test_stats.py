from math import log10
import unittest
from unittest import TestCase
import time

from stats import StatsControl

'''
Document test class

author :Alexis Fossart
date :  08/10/2017

Class used to test the document class
'''


class TestStats(TestCase):

    def setUp(self):
        '''Initialisation des tests'''
        self.ctrl = StatsControl
        self.ctrl.new_query("A B C D E")
        time.sleep(1)
        self.ctrl.last_query().stop()
        time.sleep(1)
        self.ctrl.new_query("A B C D E F")
        time.sleep(1)
        self.ctrl.last_query().stop()
        self.ctrl.new_query("A B C D ")
        self.stats = self.ctrl.last_query()

    def test_stop(self):
        self.stats.add_mem_access()
        self.stats.add_mem_access()
        self.stats.add_mem_access()
        self.stats.add_mem_access()
        time.sleep(1)
        self.stats.stop()
        for q in self.ctrl.all_queries():
            print(q)

if __name__ == "__main__":
    unittest.main()
