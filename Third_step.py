from pyspark.sql import SparkSession
from faker import Factory
from pyspark.sql.functions import udf
from pyspark.sql.types import *

fake = Factory.create('en_AU')

def fake_first_name():
    return fake.first_name()


spark = SparkSession.builder.appName('Third_step').getOrCreate()
df = spark.read.option('header',True).option('delimiter','|').option("inferSchema",True).csv("data/cvs_file.csv")
print('----------')
df.printSchema()
df.show(truncate=False)

fake_first_name_udf = udf(fake_first_name, StringType())
df1 = df.withColumn('first_name', fake_first_name_udf())
df1.show(truncate=False)