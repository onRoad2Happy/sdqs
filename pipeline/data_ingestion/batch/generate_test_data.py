import happybase

from utils.data import generate_table
import config 

batch_size = 1000
host = config.hbase_host
namespace = "sample_data"
row_count = 0
table_name = "rfic"
# file_path = "Request_for_Information_Cases.csv"


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


# After everything has been defined, run the script.

# print "Connect to HBase. table name: %s, batch size: %i" % (table_name, batch_size)
# data = generate_table(n_rows = 1000, m_cols = 2, repeated_times = 3, random_max = 5)
# for i, row in enumerate(data):
    # batch.put(str(i), { "data:a": str(row[0]), "data:b": str(row[1]) })

conn = connect_to_hbase()
# batch = table.batch(batch_size = batch_size)


def get_data(table_name):
    table = conn.table(table_name)
    return [data for key, data in table.scan()]



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

