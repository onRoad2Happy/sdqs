HDFS_PATH = "hdfs://ip-xxxxxxxx.us-west-2.compute.internal:9000/user/data/"
RETHINKDB_PATH = 'ec2-xxxxxxxxxxxxxxxxxxxxxxx.compute.amazonaws.com'

# kafka stream config and spark config

SERVER_CONFIG = {
    'master' : 'spark://xxxxxxxxxxxxxxxxxxxxxx.compute.internal:7077', 
    'app_name' : 'app'
}


BROKER_CONFIG = {
    'brokers' : ['ec2-xxxxxxxxxxxxxxxxxxxxx.compute.amazonaws.com:9092', 'ec2-xxxxxxxxxxxxxxxxxxxxxxxx.compute.amazonaws.com:9092', 'ec2-xxxxxxxxxxxxxxxxxxxxx.compute.amazonaws.com:9092'],
    'app_name' : 'stream_kafka',
}

zkQuorum = 'ec2-xxxxxxxxxxxxxxxxxxxxx.compute.amazonaws.com:2181'

HBASE_HOST = "ec2-xxxxxxxxxxxxxxxxxxxxx.compute.amazonaws.com"
NAMESPACE = "sample_data" 

BOOTSTRAP_SERVERS='ec2-xxxxxxxxxxxxxxxxxxxxx.compute.amazonaws.com:9092'

METRIC_TABLE = 'test_table'
DB_NAME = 'test'


