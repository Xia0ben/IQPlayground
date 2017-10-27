from unittest import TestCase
from executable import Executable


class TestRandomIndexing(TestCase):

    def setUp(self):
        self.exec_var = Executable()
        self.file_path = ["../latimes/la010189"]

    def test_exec_random_indexing(self):
        self.exec_var = Executable()
        self.file_path = ["../latimes/la010189"]
        self.exec_var.indexing(self.file_path)
        self.exec_var.random_indexing("washington", 10)

