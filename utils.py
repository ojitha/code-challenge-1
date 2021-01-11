import re
import ConfigParser

#constants
WIDTH ='width'
NAME = 'name'
#cleansing the pre and post \' characters
def removeStartEndChars(str):
    pre = re.sub("^\'","",str)
    post = pre[:-1]
    return post

# file confituration from config.ini files is stored here for resuablility
class FileConfig:

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')

        # first_name
        self.first_name = {NAME:config.get('FIXED_WIDTH_FILE','first_name.name')
            ,WIDTH:int(config.get('FIXED_WIDTH_FILE','first_name.width'))}
        # last_name
        self.last_name = {NAME:config.get('FIXED_WIDTH_FILE','last_name.name')
            ,WIDTH:int(config.get('FIXED_WIDTH_FILE','last_name.width'))}

        # address
        self.address = {NAME:config.get('FIXED_WIDTH_FILE','address.name')
            ,WIDTH:int(config.get('FIXED_WIDTH_FILE','address.width'))}

        # dob
        self.dob = {NAME:config.get('FIXED_WIDTH_FILE','dob.name')
            ,WIDTH:int(config.get('FIXED_WIDTH_FILE','dob.width'))}
    

    @property
    def first_name(self):
        return self.first_name

    @property
    def last_name(self):
        return self.last_name

    @property
    def address(self):
        return self.address

    @property
    def dob(self):
        return self.dob
