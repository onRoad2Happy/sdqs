from data_ingestion.batch.generate_test_data import get_data
from component.generate_simulate_data import data_toDF
from component.generate_simulate_data import get_profile_dict


def profiling(table_name, data_type):
    if data_type == 'batch':
        data = get_data()
        df = data_toDF(data, ['a', 'b'], 2)
        print get_profile_dict(df, ['a', 'b'])


