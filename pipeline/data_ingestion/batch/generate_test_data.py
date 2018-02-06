import happybase
import csv
import os
import sys
import random
# must before import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config 

batch_size = 1000

host = config.HBASE_HOST
namespace = cofig.NAMESPACE 

def get_data(table_name):
    conn = connect_to_hbase()
    table = conn.table(table_name)
    return [data for key, data in table.scan()]

def get_table(table_name):
    conn = connect_to_hbase()
    table = conn.table(table_name)
    return table

def connect_to_hbase():
    """ Connect to HBase server.
    This will use the host, namespace, table name, and batch size as defined in
    the global variables above.
    """
    host = config.hbase_host
    conn = happybase.Connection(host = host,
        table_prefix = namespace,
        table_prefix_separator = ":")
    conn.open()
    return conn

def generate_test_table(table_name, column_family, repeated_times, attrs, n_rows, random_max, batch_size, connection):
    if table_name not in connection.tables():
        connection.create_table(table_name, { column_family: dict()})
    x = 0
    i = 0
    table = connection.table(table_name)

    batch = table.batch(batch_size = batch_size)
    while i <= n_rows:
        for t in range(0, repeated_times):
            row = dict()
            row[column_family + ":" + attrs[0]] = str(x) 
            for attr in attrs[1:]:
                row[column_family + ":" + attr] = str(random.randint(1, random_max))
            batch.put(str(i), row)
            i += 1
        x = x + 1

def store_csv_to_hbase(file_name, connection, batch_size, column_family, table_name):
    if table_name not in connection.table():
        connection.create_table(table_name, {column_family: dict()})

    table = connection.table(table_name)
    batch = table.batch(batch_size = batch_size)
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        attrs = next(reader)  # gets the first line

        x = 0
        for r in reader:
            row = dict()
            row[column_family + ":" + 'id'] = str(x) 
            for i, attr in enumerate(r):
                row[column_family + ":" + attrs[i]] = str(attr)
            batch.put(str(i), row)
            x = x + 1

def generate_test_table_to_csv(file_name, repeated_times, attrs, n_rows, random_max):
    with open(file_name, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(attrs)
        x = 0
        i = 0
        while i <= n_rows:
            for t in range(0, repeated_times):
                row = list()
                row.append(x)
                for attr in attrs[1:]:
                    row.append(random.randint(1, random_max))
                writer.writerow(row)
                i += 1
            x = x + 1

if __name__ == "__main__":
    attrs = ['key', 'a', 'b', 'c', 'd']
    # conn = connect_to_hbase()
   # generate_test_table('test_table_100', 'cf', 4, attrs, 100, 10, 100, conn)
    # generate_test_table('test_table_1k', 'cf', 4, attrs, 1000, 10, 100, conn)
    # generate_test_table('test_table_1000000', 'cf', 4, attrs, 1000000, 10, 100, conn)

    # attrs = ['key', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # generate_test_table('test_table_10MX10', 'cf', 4, attrs, 10000000, 10, 1000, conn)
    # attrs = ['key', 'a', 'b', 'c', 'd']
    # n_rows = 1000000 * 100
    # generate_test_table_to_csv('test_csv_100M.csv', 4,  attrs, n_rows, 10)



