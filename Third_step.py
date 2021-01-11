```
    Third step to create anonymize csv
```

from pyspark.sql import SparkSession
from faker import Factory
from pyspark.sql.functions import udf
from pyspark.sql.types import *
import ConfigParser
import logging

logging.basicConfig(filename='today.log',level=logging.INFO)
config = ConfigParser.ConfigParser()
config.read('config.ini')

#create faker factory
fake = Factory.create('en_AU')

#user define function for the first name faker
def fake_first_name():
    return fake.first_name()
fake_first_name_udf = udf(fake_first_name, StringType())

#user define function for the last name faker
def fake_last_name():
    return fake.last_name()
fake_last_name_udf = udf(fake_last_name, StringType())

#user define function for the address faker
def fake_address():
    return fake.address().replace('\n','')
fake_address_udf = udf(fake_address, StringType())

spark = SparkSession.builder.appName('Third_step').getOrCreate()
df = spark.read.option('header',True).option('delimiter','|').option("inferSchema",True).csv("data/"+config.get('DEFAULT','csv_file.name'))
logging.info(df.printSchema())

#df.show(truncate=False)

anonymize_df = df.withColumn(config.get('FIXED_WIDTH_FILE','first_name.name'), fake_first_name_udf()) \
    .withColumn(config.get('FIXED_WIDTH_FILE','last_name.name'), fake_last_name_udf()) \
    .withColumn('address', fake_address_udf())

#anonymize_df.show(truncate=False)
anonymize_df.write.option('header',True).format('csv').save('data/'+config.get('DEFAULT','anonymize_file.name'))
