from kafka import KafkaProducer
import json
# producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(bootstrap_servers='ec2-52-32-18-38.us-west-2.compute.amazonaws.com:9092')

def generate_test_json_table():
    data = list()
    while x * repeated_times <= n_rows:
        for t in range(0, repeated_times):
            l = dict()
            l['key'] = x
            for j in range(0, m_cols):
                l[str(j)] = random.randint(1, random_max)
            data.append(l)
        x = x + 1
    return data



while(True):
    for i in range(50000):
        # producer.send('test_topic', json.dumps({'a': 2, 'b': 3, 'c': 4}))
        producer.send('test_topic', str(i) + ',' + str(i+1) + ',' + str(i+2))



