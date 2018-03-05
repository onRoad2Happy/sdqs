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

BATCH_SIZE = 16384
import random

def generate_random_stream_data(producer):
    # while(True):
    for i in range(500):
        a = random.randint(1, 10) 
        b = random.randint(10, 20)
        c = random.randint(30, 40)
        producer.send('graph', str(a) + ',' + str(b) + ',' + str(c))


def test_aggregate_data(producer):
    for i in range(50):
        producer.send('stream', str(random.randint(1, 10)) + ',' + str(i+1) + ',' + str(i+2))
        producer.send('stream', str(random.randint(1, 10)) + ',' + str(i+1) + ',' + str(i+2))
        producer.send('stream', str(random.randint(1, 10)) + ',' + str(i+1) + ',' + str(i+2))

def test_accuracy_data(producer, target, source):
    with open(target, "r") as ins:
        for line in ins:
            producer.send('user_info', 'target' +'|'+ line)
    with open(source, "r") as ins:
        for line in ins:
            producer.send('user_info', 'source' +'|'+ line)

from time import sleep
def main():
    # producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, batch_size=BATCH_SIZE, linger_ms=10)
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, batch_size=BATCH_SIZE)
    source = "../../test/users_info_src.dat.txt"
    target = "../../test/users_info_target.dat.txt"
    while True:
        sleep(5)
        test_accuracy_data(producer, target, source)
        generate_random_stream_data(producer)
        test_aggregate_data(producer)
    

if __name__ == "__main__":
    main()
