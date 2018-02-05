from pyspark import SparkConf, SparkContext
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import json
import sys
import rethinkdb as r

from batch_process import get_attributes_summary
from batch_process import get_attributes
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import time

brokers = config.BROKER_CONFIG['brokers']
APP_NAME = config.BROKER_CONFIG['app_name']
MASTER = config.SERVER_CONFIG['master']
zkQuorum = config.zkQuorum 


spark = SparkSession.builder.appName(APP_NAME).master(MASTER).getOrCreate()

def process(rdd):
    return rdd.collect()

def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

def streaming(now, rdd, topic, re_table, conn, attributes):
    try:
        tic = time.clock()
        rdd.cache()
	# print "=========%s========" % str(now)
	spark = getSparkSessionInstance(rdd.context.getConf())
	# rowRdd = rdd.map(lambda w: json.loads(w))
        result = dict()
        rowRdd = rdd.map(lambda w: w[1].split(",")).map(lambda p: Row(a= int(p[0]), b = int(p[1]), c = int(p[2])))
        df = spark.createDataFrame(rowRdd)
        summary= get_attributes(df, attributes)
        result['topic'] = topic
        result['summary'] = summary
        result['time'] = r.now().to_iso8601()
        toc = time.clock()
        result['run_time'] = toc -tic
        re_table.insert(result).run(conn)
        rdd.unpersist()

    except:
        print("Unexpected error:", sys.exc_info())
        pass
    

def show_message_size_flow(kvs):
    kvs = kvs.count()
    kvs.pprint()

def store_toDB(time_summary, result, reTable):
    result['time'] = time_summary[0]
    result['attributes'] = time_summary[1]
    reTable.insert(result)

def streaming_profile_toDB(topic, re_table, conn, attributes):
    sc = spark.sparkContext
    ssc = StreamingContext(sc, 5)
    numThread = 3
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: numThread})
    kvs.foreachRDD(lambda t, rdd: streaming(t, rdd, topic, re_table, conn, attributes))
    ssc.start()
    ssc.awaitTermination()
    # ssc.awaitTerminationOrTimeout(10)



# def main(spark):
    # sc = spark.sparkContext
    # ssc = StreamingContext(sc, 5)
    # topic = "test_topic"
    # numThread = 3
    # kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: numThread})

    # kvs.foreachRDD(streaming)

    # ssc.start()
    # ssc.awaitTermination()


# if __name__ == "__main__":
    # spark = SparkSession.builder.appName(APP_NAME).master(MASTER).getOrCreate()
    # main(spark)
