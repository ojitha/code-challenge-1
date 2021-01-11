import unittest
from utils import removeStartEndChars, FileConfig, NAME, WIDTH
import logging
import ConfigParser

class Cleansing(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.ini')

    def test_removeStartEndChars(self):
        self.assertEquals(removeStartEndChars("'Ojitha'"),'Ojitha')


    def test_FileConfig(self):
        f_config = FileConfig()
        self.assertEquals(f_config.first_name[NAME], self.config.get('FIXED_WIDTH_FILE','first_name.name') )
        self.assertEquals(f_config.first_name[WIDTH], int(self.config.get('FIXED_WIDTH_FILE','first_name.width')) )

        self.assertEquals(f_config.last_name[NAME], self.config.get('FIXED_WIDTH_FILE','last_name.name') )
        self.assertEquals(f_config.last_name[WIDTH], int(self.config.get('FIXED_WIDTH_FILE','last_name.width')) )

        self.assertEquals(f_config.address[NAME], self.config.get('FIXED_WIDTH_FILE','address.name') )
        self.assertEquals(f_config.address[WIDTH], int(self.config.get('FIXED_WIDTH_FILE','address.width')) )

        self.assertEquals(f_config.dob[NAME], self.config.get('FIXED_WIDTH_FILE','dob.name') )
        self.assertEquals(f_config.dob[WIDTH], int(self.config.get('FIXED_WIDTH_FILE','dob.width')) ) 
