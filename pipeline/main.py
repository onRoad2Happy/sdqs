from data_ingestion.batch.generate_test_data import get_data
from component.generate_simulate_data import data_toDF
from component.generate_simulate_data import get_accuracy 
from component.generate_simulate_data import get_attributes_summary 
from component.kafkaStreamToSpark import streaming_profile_toDB
import rethinkdb as r

job = {
        'target_table': 'rfic', 
        'target_id': 3, 
        'source_table': 'rfic', 
        'source_id': 4, 
        'jobs': ['profile', 'accuracy'],
        'data_type': 'batch'
    }

job = {
        'target_table': 'test_topic', 
        'target_id': 3, 
        'jobs': ['profile'],
        'data_type': 'stream'
    }

if __name__ == "__main__":
    conn = r.connect('ec2-34-209-184-21.us-west-2.compute.amazonaws.com', 28015).repl()
    stream_table_name = 'test_stream_table'
    if stream_table_name not in r.db('test').table_list().run():
        r.db('test').table_create(stream_table_name).run()

    if 'test_table' not in r.db('test').table_list().run():
        r.db('test').table_create('test_table').run()

    table_name = job['target_table']
    schema = ['a', 'b']
    result = dict()
    result['name'] = table_name
    result['type'] = list()
    result['type'].append(job['data_type'])

    if job['data_type'] == 'batch':
        result['id'] = job['target_id']
        data = get_data(table_name)
        df = data_toDF(data, schema, 2)
        for job_type in job['jobs']:
            if job_type == 'profile':
                result['type'].append('profile')
                result['attributes'] = get_attributes_summary(df, schema)

            if job_type == 'accuracy':
                source_table_name = job['source_table']
                source_data = get_data(source_table_name)
                df_s = data_toDF(source_data, schema, 2)
                accuracy = get_accuracy(df_s, df)
                result['type'].append('accuracy')
                result['source_id'] = job['source_id']
                result['source_name'] = source_table_name
                result['attributes'] = get_attributes_summary(df_s, schema)
                result['accuray'] = accuracy

    if job['data_type'] == 'stream':
        result['type'].append('stream')
        re_table = r.table(stream_table_name)

        for job_type in job['jobs']:
            if job_type == 'profile':
                # get data from hbase transform to spark then save output to rethinkdb
                result['type'].append('profile')
                topic = job['target_table']
                streaming_profile_toDB(topic, result, re_table, conn)

            if job_type == 'accuracy':
                # get second table from hbase transform to spark
                pass
            if job_type == 'anomaly':
                pass

    print result
    r.table('test_table').insert(result).run()




