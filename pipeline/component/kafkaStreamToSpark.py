
from pyspark import SparkConf, SparkContext
from pyspark.sql import Row
from pyspark.sql import SparkSession

from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from generate_simulate_data import get_attributes_summary
import config


brokers = config.BROKER_CONFIG['brokers']
APP_NAME = config.BROKER_CONFIG['app_name']
MASTER = config.SERVER_CONFIG['master']

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
import json

from pyspark.sql import Row

import sys
import rethinkdb as r
def show_profile(time, rdd, result, re_table, conn):
    try:
        # conn = r.connect('ec2-34-209-184-21.us-west-2.compute.amazonaws.com', 28015).repl() 
	print "=========%s========" % str(time)
	spark = getSparkSessionInstance(rdd.context.getConf())
	# rowRdd = rdd.map(lambda w: json.loads(w))

        rowRdd = rdd.map(lambda w: w[1].split(",")).map(lambda p: Row(a= int(p[0]), b = int(p[1]), c = int(p[2])))
        df = spark.createDataFrame(rowRdd)
        summary = get_attributes_summary(df, ['a', 'b', 'c'])
        result['attribute'] = summary
        result['time'] = r.now().to_iso8601()
        print result
        # r.table().insert(result).run(conn)
        re_table.insert(result).run(conn)
        # conn.close()
        # reTable.insert(result).run()

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

def streaming_profile_toDB(topic, result, re_table, conn):
    sc = spark.sparkContext
    ssc = StreamingContext(sc, 5)
    zkQuorum = 'ec2-52-32-18-38.us-west-2.compute.amazonaws.com:2181'
    numThread = 3
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: numThread})
    kvs.foreachRDD(lambda t, rdd: show_profile(t, rdd, result, re_table, conn))
    ssc.start()
    ssc.awaitTermination()



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
