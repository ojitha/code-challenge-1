import unittest
from GenerateFixWidthFile import createRow
import logging

class FixedWidthTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(filename='test.log', level=logging.DEBUG)

    def test_createRow_best_fit(self):
        logging.info('Best Fit:')
        f_lengths = (20,20,80,12)
        row = createRow(f_lengths,"Ojitha", "Kumanayaka", "13 Kent St, Epping, NSW, 2121", "1971-06-09")
        self.assertEqual(len(row), sum(f_lengths))

    def test_createRow_exact_fit(self):
        logging.info('Exact fit:')
        first_name = 'Gerald'
        last_name='Harris'
        address = 'Unit 64  39 Hansen Road Danielstad, VIC, 7525'
        dob = '1982-06-09'
        field_lengths = (len(first_name) ,len(last_name) ,len(address) ,len(dob))

        row = createRow(field_lengths,first_name, last_name, address, dob)
        self.assertEqual(len(row), sum(tuple(map(lambda x: x+2, field_lengths))) ) 
        #self.assertEqual(len(row), sum(field_lengths))

    def test_createRow_less_fit(self):
        logging.info('Less Fit:')
        f_lengths = (6-2,10-2,29-2,10-2)
        self.assertRaises(Exception, createRow, f_lengths,"Ojitha", "Kumanayaka", "13 Kent St, Epping, NSW, 2121", "1989-03-30")          
     