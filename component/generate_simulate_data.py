from pyspark import SparkConf, SparkContext
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id 


MASTER = 'spark://ip-10-0-0-14.us-west-2.compute.internal:7077'
APP_NAME = 'app'



import random
k_l = [1, 5, 10, 20, 100]
# when k is 1 the feild is distinct
# when k is bigger it means data has more repeated keys 

data = list()
n_rows = 1000000
m_cols = 2
n_partition = 3

rows = [10000, 100000, 10000000]
repeated_times_l = [1, 10, 50]

x = 0
repeated_times = 3
random_max = 20

def generate_table(n_rows, m_cols, repeated_times, random_max):
    data = list()
    x = 0
    while x * repeated_times <= n_rows:
        for t in range(0, repeated_times):
            l = list()
            l.append(x)
            for j in range(0, m_cols):
                l.append(random.randint(1, random_max))
            data.append(l)
        x = x + 1
    return data

def getAccuracy(realDF, targetDF):
    return 1.0 - realDF.subtract(targetDF).count() * 1.0 / realDF.count()
   
def getSize(df):
    return df.count()

def write_parquet(df, dest):
    #df.write.partitionBy("key").format("parquet").save(dest)
    df.write.parquet(dest)
    
import time

def main(spark):
    sc = spark.sparkContext
    for repeated_times in repeated_times_l:
	
        data = generate_table(n_rows, m_cols, repeated_times, random_max)
        rdd = sc.parallelize(data, n_partition)
        dataDF = spark.createDataFrame(rdd, schema=['key', 'a', 'b'])
        #write_parquet(dataDF, 'test_' + str(n_row) + '.parquet')
        #dataDF = spark.read.parquet('test_' + str(n_row) + '.parquet')
        #dataDF.createOrReplaceTempView("parquetFile")
    
    #rdd = sc.parallelize(data, n_partition)
    #dataDF = spark.createDataFrame(rdd, schema=['key', 'a', 'b'])
    #profile(dataDF, ['key', 'a'])
    #print 'size'
    #print getSize(dataDF)
	start_time = time.time()
        print 'number of repeated times: ' + str(repeated_times)
    	print 'accuracy  ' + str(getAccuracy(dataDF, dataDF))
	print("--- %s seconds ---" % (time.time() - start_time))
        profile(dataDF, ['key', 'a'])



def profile(df, attrs):
    df.describe(attrs).show()
    


if __name__ == "__main__":
        # Configure OPTIONS
    spark = SparkSession.builder.appName(APP_NAME).master(MASTER).getOrCreate()
    main(spark)
    

    #conf = SparkConf().setAppName(APP_NAME).setMaster(MASTER)
    #sc = SparkContext(conf=conf)
    #main(sc)


