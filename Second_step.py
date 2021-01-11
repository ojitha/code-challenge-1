'''
    This script creates the CSV file from the fix width file using
    PySpark. This has to be executed in the Hortonwork sandbox version 2.6.
'''

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from utils import removeStartEndChars, FileConfig, WIDTH, NAME
import ConfigParser
import logging

logging.basicConfig(filename='today.log',level=logging.INFO)

f_config = FileConfig()

config = ConfigParser.ConfigParser()
config.read('config.ini')

# created a UDF to cleanse for example
cleanCol = udf(lambda x: removeStartEndChars(x), StringType())

spark = SparkSession.builder.appName('abc').getOrCreate()

df = spark.read.text("data/"+config.get('FIXED_WIDTH_FILE','file_name'))

#create a dataframe from the fixed width file
csv_df = df.select(
    df.value.substr(1
        ,f_config.first_name[WIDTH]).alias(f_config.first_name[NAME]),
    df.value.substr(f_config.first_name[WIDTH]+1
        ,f_config.last_name[WIDTH]).alias(f_config.last_name[NAME]),
    df.value.substr(f_config.first_name[WIDTH]+f_config.last_name[WIDTH]+1
        ,f_config.address[WIDTH]).alias(f_config.address[NAME]),
    df.value.substr(f_config.first_name[WIDTH]+f_config.last_name[WIDTH]+f_config.address[WIDTH]+1
        ,f_config.dob[WIDTH]).alias(f_config.dob[NAME])
)
# csv_df.show()
df_to_save = csv_df \
    .withColumn(f_config.first_name[NAME], cleanCol(f_config.first_name[NAME])) \
    .withColumn(f_config.last_name[NAME], cleanCol(f_config.last_name[NAME])) \
    .withColumn(f_config.address[NAME], cleanCol(f_config.address[NAME])) \
    .withColumn(f_config.dob[NAME], cleanCol(f_config.dob[NAME]))

# integrity check
if int(df_to_save.count()) != int(config.get('DEFAULT','number_of_records')):
    logging.error("Integrity check failed because data frame record count is %d and expected count is %d",df_to_save.count(), int(config.get('DEFAULT','number_of_records') ))
else:
    logging.info('Integrity check passed.')
df_to_save.write.option('delimiter','|').option('header',True).format('csv').save('data/'+config.get('DEFAULT','csv_file.name'))
