from faker import Factory
import configparser
import logging

# method to create row of data
def createRow(f_lengths, first_name,last_name,address, dob):
    logging.debug('Field lengths: %s', f_lengths)

    format_str = "{0!a:<%ss}{1!a:<%ss}{2!a:<%ss}{3!a:<%ss}" % f_lengths
     
    row = format_str.format(first_name,last_name, address, dob)
    file_width = sum(tuple(map(lambda x: x+2,f_lengths))) # ASCII conversion:+2 for char \' at the ends of each field
    logging.debug('row: "%s".' % row)
    logging.debug('current row length is %d, File width is %d', len(row), file_width)
    
    # verify the row length against the file fix width
    if len(row) > file_width:
        logging.error("Not Fit: row length %d > File width %d" % (len(row), file_width))
        raise Exception("Current row length %d excceded the width %d  of the file." % (len(row), file_width))
    return row

#Create a fix width file using the definitions given in the config.ini file
def main():

    # Read the column width 
    config = configparser.ConfigParser()
    config.read('config.ini')
    logging.basicConfig(filename=config['DEFAULT']['logging.file'], level=logging.DEBUG)

    # AU compatible data file
    fake = Factory.create('en_AU')
    print("--- Processing file '%s' according to the specification given in the config.ini ---" % config['FIXED_WIDTH_FILE']['file_name'])
    print(" NOTE: For more information, see the log %s file" % config['DEFAULT']['logging.file']) 

    with open(config['FIXED_WIDTH_FILE']['file_name'], encoding="ascii",mode='a') as f: # find the filename in the config.ini file
        f_lens = (
        int(config['FIXED_WIDTH_FILE']['first_name.width'])
        , int(config['FIXED_WIDTH_FILE']['last_name.width'])
        , int(config['FIXED_WIDTH_FILE']['address.width'])
        , int(config['FIXED_WIDTH_FILE']['dob.width'])
        )
        for _ in range(int(config['DEFAULT']['number_of_records'])):
            print(createRow(f_lens,fake.first_name(),fake.last_name(),fake.address().replace('\n',' '),fake.date()), file=f)

    logging.info("Created fix width %d ASCII chars %s with %d records" %(sum(tuple(map(lambda x: x+2,f_lens)))
        ,config['FIXED_WIDTH_FILE']['file_name'],int(config['DEFAULT']['number_of_records'])))
       
    print("--- End ---")

if __name__ == "__main__":
    main()