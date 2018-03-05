import time
import random
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


from pyspark import SparkConf, SparkContext
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.sql.types import LongType, StringType, StructField, StructType, BooleanType, ArrayType, IntegerType
from pyspark.mllib.random import RandomRDDs

MASTER = config.SERVER_CONFIG['master']
APP_NAME = config.SERVER_CONFIG['app_name'] 
# spark = SparkSession.builder.appName(APP_NAME).master(MASTER).getOrCreate()
spark = SparkSession.builder.appName(APP_NAME).getOrCreate()


def hdfs_toDF(path, has_header=True, attributes=None):
    schema = None
    if attributes:
        schema = StructType([StructField(key, StringType(), True) for key in attributes])

    if has_header:
        return spark.read.option("header","true").option("inferSchema", "true").option("nullValue", "NA").csv(path) 
    else:
        return spark.read.option("header", "false").schema(schema).csv(path) 


def generate_table(n_rows, m_cols, repeated_times, random_max):
    data = list()
    x = 0
    while x * repeated_times <= n_rows:
        for t in range(0, repeated_times):
            l = list()
            l.append(x)
            for j in range(0, m_cols):
                l.append(random.randint(1, random_max))
            data.append(l)
        x = x + 1
    return data

def get_accuracy(realDF, targetDF):
    return 1.0 - realDF.subtract(targetDF).count() * 1.0 / realDF.count()

   
def getSize(df):
    return df.count()

    
def data_toDF(data, schema, n_partition):
    sc = spark.sparkContext
    rdd = sc.parallelize(data, n_partition)
    dataDF = spark.createDataFrame(rdd, schema=schema)
    return dataDF

def table_toDF(table, schema, n_partition):
    sc = spark.sparkContext
    rdd = sc.parallelize([data for key, data in table.scan()], n_partition)
    dataDF = spark.createDataFrame(rdd, schema=schema)
    return dataDF

def profile(df, attrs):
    df.describe(attrs).show()

# {'a': {0: u'1000050', 1: u'10.501937903104844', 2: u'5.764012905602232', 3: u'1', 4: u'20'}, 'key': {0: u'1000050', 1: u'10000.0', 2: u'5773.794246567651', 3: u'0', 4: u'20000'}, 'summary': {0: u'count', 1: u'mean', 2: u'stddev', 3: u'min', 4: u'max'}}{'a': {0: u'1000050', 1: u'10.501937903104844', 2: u'5.764012905602232', 3: u'1', 4: u'20'}, 'key': {0: u'1000050', 1: u'10000.0', 2: u'5773.794246567651', 3: u'0', 4: u'20000'}, 'summary': {0: u'count', 1: u'mean', 2: u'stddev', 3: u'min', 4: u'max'}}i

def get_attributes_summary(df, attrs):
    data = None
    if attrs is None:
        data = df.describe().toPandas().to_dict()
    else:
        data = df.describe(attrs).toPandas().to_dict()

    for attr in data:
        if attr != 'summary':
            summary = data[attr]
            summary['count'] = summary.pop(0)
            summary['mean'] = summary.pop(1)
            summary['stddev'] = summary.pop(2)
            summary['min'] = summary.pop(3)
            summary['max'] = summary.pop(4)
    data.pop('summary')

    attributes = list()
    for attr in data:
        data[attr]['name'] = attr 
        attributes.append(data[attr])
    return attributes

def get_user_defined_profile(df, rule):
    df.createOrReplaceTempView('target')
    summary = spark.sql(rule)
    return summary.toPandas().to_dict('records')

def get_attributes(df, attrs):
    data = df.describe(attrs).toPandas().to_dict()
    for attr in data:
        if attr != 'summary':
            summary = data[attr]
            summary['count'] = summary.pop(0)
            summary['mean'] = summary.pop(1)
            summary['stddev'] = summary.pop(2)
            summary['min'] = summary.pop(3)
            summary['max'] = summary.pop(4)
    data.pop('summary')
    return data



def toCSVLine(data):
    # return ','.join(str(int(d* 10)) for d in data)
    return ','.join(str(d)for d in data)

def generate_csv_hdfs(spark, row, col, path, num_partition=3):
    sc = spark.sparkContext
    rdd = RandomRDDs.uniformVectorRDD(sc, row, col, num_partition)
    lines = rdd.map(toCSVLine)
    lines.saveAsTextFile(path)

def main(spark):
    path = "hdfs://ip-10-0-0-9.us-west-2.compute.internal:9000/user/data/"
    # file_name = 'test_csv_6G.csv'
    # generate_csv_hdfs(spark, 6000000000L, 5,  path + file_name)
    file_name = 'test_csv_1.4G.csv'
    generate_csv_hdfs(spark, 1400000000, 5,  path + file_name)


    # df = hdfs_toDF(path + file_name, False,  ['a', 'b', 'c', 'd', 'e'])
    # df.show()

if __name__ == "__main__":
    main(spark)

