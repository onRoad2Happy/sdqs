import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config

from kafka import KafkaProducer


BOOTSTRAP_SERVERS = config.BOOTSTRAP_SERVERS

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

def main():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    while(True):
        for i in range(50000):
            # producer.send('test_topic', json.dumps({'a': 2, 'b': 3, 'c': 4}))
            producer.send('test_topic', str(i) + ',' + str(i+1) + ',' + str(i+2))



if __name__ == "__main__":
    main()
