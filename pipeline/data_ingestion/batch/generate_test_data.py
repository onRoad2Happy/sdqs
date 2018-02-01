import happybase
import csv
import config 
import random
from utils.data import generate_table
batch_size = 1000
host = config.hbase_host
namespace = "sample_data"

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
    # generate_test_table('test_table_10000', 'cf', 4, attrs, 10000, 10, 100, conn)
    # generate_test_table('test_table_1000000', 'cf', 4, attrs, 1000000, 10, 100, conn)

    attrs = ['key', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    # generate_test_table('test_table_10MX10', 'cf', 4, attrs, 10000000, 10, 1000, conn)
    attrs = ['key', 'a', 'b', 'c', 'd']
    generate_test_table_to_csv('test_csv_1k.csv', 4,  attrs, 1000, 10)
# After everything has been defined, run the script.


# def read_csv():
    # csvfile = open(file_path, "r")
    # csvreader = csv.reader(csvfile)
    # return csvreader, csvfile

    

# def insert_row(batch, row):
    # """ Insert a row into HBase.
    # Write the row to the batch. When the batch size is reached, rows will be
    # sent to the database.
    # Rows have the following schema:
        # [ id, keyword, subcategory, type, township, city, zip, council_district,
          # opened, closed, status, origin, location ]
    # """
    # batch.put(row[0], { "data:kw": row[1], "data:sub": row[2], "data:type": row[3],
        # "data:town": row[4], "data:city": row[5], "data:zip": row[6],
        # "data:cdist": row[7], "data:open": row[8], "data:close": row[9],
        # "data:status": row[10], "data:origin": row[11], "data:loc": row[12] })

# csvreader, csvfile = read_csv()
# print "Connected to file. name: %s" % (file_path)


# try:
    # # Loop through the rows. The first row contains column headers, so skip that
    # # row. Insert all remaining rows into the database.
    # for row in csvreader:
        # row_count += 1
        # if row_count == 1:
            # pass
        # else:
            # insert_row(batch, row)

    # # If there are any leftover rows in the batch, send them now.
    # batch.send()
# finally:
    # # No matter what happens, close the file handle.
    # csvfile.close()
    # conn.close()

