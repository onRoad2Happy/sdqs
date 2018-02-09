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

print BOOTSTRAP_SERVERS
BATCH_SIZE = 16384
def main():
    # producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, batch_size=BATCH_SIZE, linger_ms=10)
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, batch_size=BATCH_SIZE)
    while(True):
        for i in range(50000):
                producer.send('stream', str(i) + ',' + str(i+1) + ',' + str(i+2))
            # producer.send('test_topic', json.dumps({'a': 2, 'b': 3, 'c': 4}))



if __name__ == "__main__":
    main()
