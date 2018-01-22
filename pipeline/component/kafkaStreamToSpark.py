
from pyspark import SparkConf, SparkContext
from pyspark.sql import Row
from pyspark.sql import SparkSession

from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import config


brokers = config.BROKER_CONFIG['brokers']
APP_NAME = config.BROKER_CONFIG['app_name']
MASTER = config.SERVER_CONFIG['master']

def process(rdd):
    return rdd.collect()

def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]
import json

from pyspark.sql import Row


def show_profile(time, rdd):
    try:
	print "=========%s========" % str(time)
	spark = getSparkSessionInstance(rdd.context.getConf())

	# rowRdd = rdd.map(lambda w: json.loads(w))

        rowRdd = rdd.map(lambda w: w[1].split(",")).map(lambda p: Row(a= int(p[0]), b = int(p[1]), c = int(p[2])))
        df = spark.createDataFrame(rowRdd)
        df.describe().show()

    except:
        pass
    

def show_message_size_flow(kvs):
    kvs = kvs.count()
    kvs.pprint()


def main(spark):
    sc = spark.sparkContext

    ssc = StreamingContext(sc, 5)
    topic = "test_topic"
    zkQuorum = 'ec2-52-32-18-38.us-west-2.compute.amazonaws.com:2181'
    numThread = 3
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: numThread})

    kvs.foreachRDD(show_profile)


    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    spark = SparkSession.builder.appName(APP_NAME).master(MASTER).getOrCreate()
    main(spark)
