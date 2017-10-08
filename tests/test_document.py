from math import log10
import unittest
from unittest import TestCase

from files import Document

'''
Document test class

author :Alexis Fossart
date :  08/10/2017

Class used to test the document class
'''


class TestDocument(TestCase):

    def setUp(self):
        '''Initialisation des tests'''
        self.document = Document("a a a a a a a a a a b c d e")

    def test_set(self):
        res = {"a", "b", "c", "d", "e"}
        self.assertEqual(res, self.document.set_of_terms())

    def test_docid(self):
        res = "a"
        self.assertEqual(res, self.document.doc_id())

    def test_tf(self):
        res = 1 + log10(10)
        self.assertEqual(res, self.document.term_frequecy("a"))


if __name__ == "__main__":
    unittest.main()
