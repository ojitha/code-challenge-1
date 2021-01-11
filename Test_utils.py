import unittest
from utils import removeStartEndChars
import logging

class Cleansing(unittest.TestCase):
    # def setUp(self):
    #     logging.basicConfig(filename='test.log', level=logging.DEBUG)

    def test_removeStartEndChars(self):
        print(removeStartEndChars("'Ojitha'"))
