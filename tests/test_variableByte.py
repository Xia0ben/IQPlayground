from algorithm import VariableByte
from unittest import TestCase


class TestVariableByte(TestCase):

    def setUp(self):
        self.numbers_input = [777, 1234, 2551, 16]
        self.byte_input = b'\x06\x89\t\xd2\x13\xf7\x90'

    def test_encoding(self):
        res = b'\x06\x89\t\xd2\x13\xf7\x90'
        self.assertEqual(res, VariableByte.encoding(self.numbers_input))

    def test_decoding(self):
        res = [777, 1234, 2551, 16]
        self.assertEqual(res, VariableByte.decoding(self.byte_input))