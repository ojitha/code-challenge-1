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
