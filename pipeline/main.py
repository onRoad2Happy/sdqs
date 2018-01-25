from data_ingestion.batch.generate_test_data import get_data
from component.generate_simulate_data import data_toDF
from component.generate_simulate_data import get_accuracy 
from component.generate_simulate_data import get_attributes_summary 


job = {
        'target_table': 'rfic', 
        'target_id': 3, 
        'source_table': 'rfic', 
        'source_id': 4, 
        'jobs': ['profile', 'accuracy'],
        'data_type': 'batch'
    }

if __name__ == "__main__":
    table_name = job['target_table']
    source_table_name = job['source_table']
    schema = ['a', 'b']
    result = dict()
    result['id'] = job['target_id']
    result['type'] = list()
    if job['data_type'] == 'batch':
        data = get_data(table_name)
        df = data_toDF(data, schema, 2)
        result['type'].append('batch')
        for job_type in job['jobs']:
            if job_type == 'profile':
                result['type'].append('profile')
                result['attributes'] = get_attributes_summary(df, schema)

            if job_type == 'accuracy':
                source_data = get_data(source_table_name)
                df_s = data_toDF(source_data, schema, 2)
                accuracy = get_accuracy(df_s, df)
                result['type'].append('accuracy')
                result['source_id'] = job['source_id']
                result['attributes'] = get_attributes_summary(df_s, schema)
                result['accuray'] = accuracy

    if job['data_type'] == 'stream':
        result['type'].append('stream')

        for job_type in job['jobs']:
            if job_type == 'profile':
                # get data from hbase transform to spark then save output to rethinkdb
                pass

            if job_type == 'accuracy':
                # get second table from hbase transform to spark
                pass
            if job_type == 'anomaly':
                pass

    print result



    



                

