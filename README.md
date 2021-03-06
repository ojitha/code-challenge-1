# Anonymize ETL

This ETL flow runs in three steps, as shown in the following diagram. The complete configuration of the fix width file is given in the `config.ini` under the section `[FIXED_WIDTH_FILE]`. In addition to that `first-file.txt` with the intermediate `csv-file.csv` and the anonymize file `anonymize.csv` are defined as properties in the section `[DEFAULT]`: you can change the file names as you want via config.ini configuration file. To increase the file size, change the `number_of_records` property to higher number.



![image-20210111165856129](https://cdn.jsdelivr.net/gh/ojitha/blog@master/uPic/image-20210111165856129.png)

Above diagram, the script to run in each step are given. You have to follow the step one after another sequence to get the final result `anonymize.csv`.



### Integrity checking

As shown in the `config.ini` under the `DEFAULT` section, the `number_of_records` property defines the expected number of records to flow in the ETL. Both the step 1 & 2, integrity check will be done and record to the `loggin.file` (that is today.log).

## Step 1

Use the docker-compose to create a Docker container using given Dockerfile. The docker composer will map your current directory to the container. When the GenerateFixWidthFile.py ran, the target text file will be created in your current directory in the local workspace.

![image-20210111191706225](https://cdn.jsdelivr.net/gh/ojitha/blog@master/uPic/image-20210111191706225.png)

To run in the docker container (This has been tested in the MacOS)

```bash
docker-compose up --build
```
In my vscode workspace:

![image-20210111105650133](https://cdn.jsdelivr.net/gh/ojitha/blog@master/uPic/image-20210111105650133.png)

As shown in the above screenshot, the data file is created (in this case `first_file.txt`) which is in fixed width. The console shows the docker-compose logs.

### Testing edge cases
```bash
python -m unittest Test_GenerateFixWidthFile.py
```
Current test cases tested three cases:

### Best Fit
This is the best scenario where row length is always less than the File width.

```
INFO:root:Best Fit:
DEBUG:root:Field lengths: (20, 20, 80, 12)
DEBUG:root:format string: {0!a:<20s}{1!a:<20s}{2!a:<80s}{3!a:<12s}
DEBUG:root:current row length is 132, File width is 140
```

### Exact Fit
This is the boundary test

```
INFO:root:Exact fit:
DEBUG:root:Field lengths: (6, 10, 29, 10)
DEBUG:root:format string: {0!a:<6s}{1!a:<10s}{2!a:<29s}{3!a:<10s}
DEBUG:root:current row length is 63, File width is 63
```

### Less Fit
This is the opposite of the first test case.

```
INFO:root:Less Fit:
DEBUG:root:Field lengths: (4, 8, 27, 8)
DEBUG:root:format string: {0!a:<4s}{1!a:<8s}{2!a:<27s}{3!a:<8s}
DEBUG:root:current row length is 63, File width is 55
ERROR:root:Not Fit: row length 63 > File width 55
```

You have to copy this file to the [hortonwork sandbox HDP](https://www.cloudera.com/downloads/hortonworks-sandbox.html) sandbox version 2.6. 

NOTE: I have used python faker package to create data.

## Step 2

This step creates intermediate CSV file (as in the `config.ini`, the file name is `csv_file.csv`). The separator of this file is unix pipe character instead of the comma. The comma character is avoided because the fixed-length file doesn't have restrictions for commas.

The script `Second_step.py` written to run in Apache Spark 2.  the reason is the version supported by the sandbox. First, the fixed-width file has to be copied to the sand box via scp. I used the standard `maria_dev` account to run this script in the sandbox. 

```bash
scp -P 2222 /path/to/first_file.txt  maria_dev@localhost:
```

Copy the following files as well:

- Second_step.py
- requirments.py
- utils.py
- config.ini

now login to the sandbox:

```bash
ssh maria_dev@localhost -p 2222
```

first create data directory in HDFS:

```bash
hdfs dfs -mkdir data
```

Then copy the `first_file.txt` to the `data` directory:

```bash
hdfs dfs -put first_file.txt data
```

Now you are ready to submit the PySpark job:

```bash
spark-submit Second_step.py
```

![image-20210111192146374](https://cdn.jsdelivr.net/gh/ojitha/blog@master/uPic/image-20210111192146374.png)

As shown in the above you have completed the step 2. The fix width file `first_file.txt` copied from the local workspace. As you see you have `csv_file.csv` as input to the last step.

## Step 3

In this step anonymize the data of the `csv_file.csv` to `anonymize.csv`. You have to run the Aparch Spark job.

First you have to copy the Thrid_step.py to the sandbox:

```bash
scp -P 2222 /path/to/Third_step.py  maria_dev@localhost:
```

Next submit PySpark job to Apache Spark:

```bash
spark-submit Third_step.py
```

You can copy the hdfs data to you local driver:

```bash
hdfs dfs -get data/anonymize.csv
```

You can verify.

IMPORTANT: Please verify integrity check is passed after the ETL process. This information is available in the log file (today.log). 

## Verify

You can verify the data loading to the hive table as follows:

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS user_data(
    first_name STRING, second_name STRING, address STRING, dob STRING)
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '|'
    STORED AS TEXTFILE
    location 'hdfs://172.18.0.2:8020/user/maria_dev/data/anonymize.csv';
```

Now use standard SQL to query the data in the `user_data` table.