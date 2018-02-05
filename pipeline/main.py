from data_ingestion.batch.generate_test_data import get_data
from data_ingestion.batch.generate_test_data import get_table
from component.batch_process import data_toDF
from component.batch_process import get_accuracy 
from component.batch_process import get_attributes_summary 
from component.stream_process import streaming_profile_toDB
from component.batch_process import hdfs_toDF 

import rethinkdb as r
import config
import os
import time
import argparse
import json


HDFS_PATH = config.HDFS_PATH
RETHINKDB_PATH = config.RETHINKDB_PATH 

def create_table_if_not_exist(db_name, table_name, conn):
    if table_name not in r.db(db_name).table_list().run(conn):
        r.db(db_name).table_create(table_name).run(conn)


def create_insert(db_name, table_name, result, conn):
    create_table_if_not_exist(db_name, table_name, conn)
    if result:
        r.table(table_name).insert(result).run(conn)
    else:
        print 'there is no content to insert'

def get_num_tables(db_name, table_name, conn):
    return r.db(db_name).table(table_name).count().run(conn)

def submit_batch_job(conn, db_name, metric_table, job, num_tables):
    result = dict()
    if 'target_id' in job:
        result['id'] = job['target_id'] 
    else:
        result['id'] = num_tables + 1

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
            result['accuracy'] = get_accuracy(df_s, df)

    create_insert(db_name, metric_table, result, conn)

def submit_stream_job(conn, db_name, metric_table, job, num_tables):
    result = dict()
    if 'target_id' in job:
        result['id'] = job['target_id'] 
    else:
        result['id'] = num_tables + 1


    result['stream_name'] = job['target_table']
    result['jobs'] = job['jobs']
    result['type'] = job['data_type']
    result['attributes'] = job['attributes']
    create_insert(db_name, metric_table, result, conn)
    create_table_if_not_exist(db_name, job['target_table'], conn)

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

def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x

from pprint import pprint


if __name__ == "__main__":

    tic = time.clock()
    conn = r.connect(RETHINKDB_PATH, 28015).repl()
    metric_table = 'test_table'
    db_name = 'test'

    num_tables = get_num_tables(db_name, metric_table, conn)

    parser = argparse.ArgumentParser(description="adding job for data quality test")
    parser.add_argument("-i", "--input", dest="file_path", required=True, 
            type=extant_file, help="required the job json file")
    args = parser.parse_args()
    print args.file_path

    job = json.load(open(args.file_path))
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print ROOT_DIR

    # if job['data_type'] == 'batch':
        # submit_batch_job(conn, db_name, metric_table, job, num_tables)
    # if job['data_type'] == 'stream':
        # submit_stream_job(conn, db_name, metric_table, job, num_tables)
    # toc = time.clock()
    # print 'run time '
    # print toc - tic

