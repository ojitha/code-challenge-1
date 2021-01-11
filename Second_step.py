'''
    This script creates the CSV file from the fix width file using
    PySpark. This has to be executed in the Hortonwork sandbox version 2.6.
'''
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from utils import removeStartEndChars


# created a UDF to cleanse for example
cleanCol = udf(lambda x: removeStartEndChars(x), StringType())

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
df_to_save = csv_df \
    .withColumn('first_name', cleanCol('first_name')) \
    .withColumn('last_name', cleanCol('last_name')) \
    .withColumn('address', cleanCol('address')) \
    .withColumn('dob', cleanCol('dob'))

df_to_save.write.option('delimiter','|').format('csv').save('data/mytest.csv')
