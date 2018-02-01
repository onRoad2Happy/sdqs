from data_ingestion.batch.generate_test_data import get_data
from data_ingestion.batch.generate_test_data import get_table
from component.generate_simulate_data import data_toDF
from component.generate_simulate_data import table_toDF 
from component.generate_simulate_data import get_accuracy 
from component.generate_simulate_data import get_attributes_summary 
from component.kafkaStreamToSpark import streaming_profile_toDB
from component.generate_simulate_data import hdfs_toDF 

import rethinkdb as r

HDFS_PATH = "hdfs://ip-10-0-0-9.us-west-2.compute.internal:9000/user/data/"

job = {
        'target_table': 'rfic', 
        'target_id': 2, 
        'jobs': ['profile', 'accuracy'],
        'data_type': 'batch', 
        'attributes': ['a', 'b'], 
        'source_table': 'rfic', 
        'source_id': 4, 
    }

# job = {
        # 'target_table': 'test_topic', 
        # 'target_id': 1, 
        # 'jobs': ['profile'],
        # 'data_type': 'stream', 
        # 'attributes': ['a', 'b', 'c']
    # }

job = {
        'target_table': 'test_table_1000000', 
        'target_id': 4, 
        'jobs': ['profile'],
        'data_type': 'batch', 
        'attributes': ['key', 'a', 'b', 'c', 'd'], 
    }

job = {
        'target_table': 'test_table_10MX10', 
        'target_id': 5, 
        'jobs': ['profile'],
        'data_type': 'batch', 
        'attributes': ['key', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'] , 
    }

job = {
        'target_table': 'test_csv_1k.csv', 
        'target_id': 6, 
        'jobs': ['profile'],
        'data_type': 'batch', 
        'attributes': ['key', 'a', 'b', 'c', 'd'] , 
        'format': 'hdfs'
    }

job = {
        'target_table': 'test_topic', 
        'target_id': 1, 
        'jobs': ['profile'],
        'data_type': 'stream', 
        'attributes': ['a', 'b', 'c']
    }


def create_table_if_not_exist(db_name, table_name):
    if table_name not in r.db(db_name).table_list().run():
        r.db(db_name).table_create(table_name).run()


def create_insert(db_name, table_name, result):
    create_table_if_not_exist(db_name, table_name)
    if result:
        r.table(table_name).insert(result).run()
    else:
        print 'there is no content to insert'
if __name__ == "__main__":
    conn = r.connect('ec2-34-209-184-21.us-west-2.compute.amazonaws.com', 28015).repl()
    metric_table = 'test_table'
    db_name = 'test'

    if job['data_type'] == 'batch':
        result = dict()
        result['id'] = job['target_id']
        result['name'] = job['target_table']
        result['type'] = job['data_type']
        result['jobs'] = job['jobs']
        result['attributes'] = job['attributes']
        attributes = result['attributes']
        df = None
        if job['format'] == 'hdfs':
            path = HDFS_PATH + job['target_table']
            df = hdfs_toDF(path)
        else:
            data = get_data(job['target_table'])
            df = data_toDF(data, attributes, 2)

        for job_type in job['jobs']:
            if job_type == 'profile':
                result['summary'] = get_attributes_summary(df, attributes)

            if job_type == 'accuracy':
                source_data = get_data(job['source_table'])
                df_s = data_toDF(source_data, attributes, 2)
                result['source_id'] = job['source_id']
                result['source_name'] = job['source_table'] 
                result['source_summary'] = get_attributes_summary(df_s, attributes)
                result['accuracy'] = round(get_accuracy(df_s, df), 4)

        create_insert(db_name, metric_table, result)

    if job['data_type'] == 'stream':
        result = dict()
        result['id'] = job['target_id']
        result['stream_name'] = job['target_table']
        result['jobs'] = job['jobs']
        result['type'] = job['data_type']
        result['attributes'] = job['attributes']
        create_insert(db_name, metric_table, result)
        create_table_if_not_exist(db_name, job['target_table'])

        for job_type in job['jobs']:
            if job_type == 'profile':
                # get data from hbase transform to spark then save output to rethinkdb
                re_table = r.table(job['target_table'])
                streaming_profile_toDB(job['target_table'], re_table, conn, job['attributes'])

            if job_type == 'accuracy':
                # get second table from hbase transform to spark
                pass

            if job_type == 'anomaly':
                pass

