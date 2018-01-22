from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
import config
MASTER = config.SERVER_CONFIG['master']
APP_NAME = config.SERVER_CONFIG['app_name'] 


spark = SparkSession.builder.appName(APP_NAME).master(MASTER).getOrCreate()
 
sc = spark.sparkContext

sqlc = SQLContext(sc)

data_source_format = 'org.apache.spark.sql.execution.datasources.hbase'

df = sc.parallelize([('a', '1.0'), ('b', '2.0')]).toDF(schema=['col0', 'col1'])

# ''.join(string.split()) in order to write a multi-line JSON string here.
catalog = ''.join("""{
    "table":{"namespace":"default", "name":"testtable"},
    "rowkey":"key",
    "columns":{
        "col0":{"cf":"rowkey", "col":"key", "type":"string"},
        "col1":{"cf":"cf", "col":"col1", "type":"string"}
    }
}""".split())

catalog = ''.join("""{
    "table":{"namespace":"sample_data", "name":"rfic"},
    "rowkey":"key",
    "columns":{
        "col0":{"cf":"rowkey", "col":"key", "type":"string"},
        "col1":{"cf":"data", "col":"a", "type":"string"}, 
        "col2":{"cf":"data", "col":"b", "type":"string"}
    }
}""".split())


# Writing
# df.write.options(catalog=catalog).format(data_source_format).save()

# Reading
df = sqlc.read.options(catalog=catalog).format(data_source_format).load()

print df.describe().show()
