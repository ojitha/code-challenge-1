'''
    This script creates the CSV file from the fix width file using
    PySpark. This has to be executed in the Hortonwork sandbox version 2.6.
'''
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import udf

spark = SparkSession.builder.appName('abc').getOrCreate()

df = spark.read.text("data/first_file.txt")

#create a dataframe from the fixed width file
csv_df = df.select(
    df.value.substr(1,20).alias('first_name'),
    df.value.substr(21,20).alias('last_name'),
    df.value.substr(41,80).alias('address'),
    df.value.substr(121,12).alias('dob')
)
csv_df.show()
csv_df.write.format('csv').save('data/mytest.csv')
