from data_ingestion.batch.generate_test_data import get_data
from component.generate_simulate_data import data_toDF
data = get_data()
data_toDF(data, ['a', 'b'], 2).describe().show()


