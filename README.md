# shawn's data quality service
data quality is important not only in batch processing but also in streaming, I want to provide a plateform for users to do data quality test for their dataset in Hbase, HDFS, kafka streaming.



## Getting Started

```
spark-submit main.py -i jobs/batch_1k.json
```


### Prerequisites

python 2.7, node 9.4.0, npm

for data pipeline
Hbase, Spark, Hadoop, kafka

for web app
Angular cli, socket io, redis, rethinkdb



### Installing

For Hbase, Spark, Hadoop

you can use the https://github.com/InsightDataScience/pegasus
to set up environment

I use 
4 m4.large for hadoop, hbase and kafka
3 m4.large for spark
2 m4.large for web app and rethinkdb

After setting up environment

fill up the evirionment setting in config_example.py
then

```
mv config_example.py config.py
```


It is better to use virtual environment for python like miniconda
python package for kafka and hbase



```
pip install -r requirements.txt
```

rethinkDB

```
https://www.rethinkdb.com/docs/install/ubuntu/
ubuntu@ip-10-0-0-7:~$ rethinkdb --bind all
ubuntu@ip-10-0-0-11:~$ rethinkdb --join SERVER_IP:29015 --bind all

```

To set up Node.js on your Linux instance (AWS)


```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.6/install.sh | bash
. ~/.nvm/nvm.sh
nvm install 

nvm install 9.4.0
node -e "console.log('Running Node.js ' + process.version)"

```
This should display the following message that confirms the installed version of Node.js running.


To install redis

```
wget http://download.redis.io/releases/redis-3.2.6.tar.gz

tar xzf redis-3.2.6.tar.gz

cd redis-3.2.6

make

sudo make install

cd utils

sudo ./install_server.sh


```

Install Nginx
```

(For ubuntu 16.04) Add following two lines into /etc/apt/sources.list

deb http://nginx.org/packages/ubuntu/ xenial nginx

deb-src http://nginx.org/packages/ubuntu/ xenial nginx

Then run:

sudo apt-get update

sudo apt-get install nginx

```



End with an example of getting some data out of the system or using it for a little demo

## Running the tests
Before running job, 
in batch, need to make sure we have the table in hbase or in hdfs
in stream, need to make sure the producer is started


### To run batch job
```
spark-submit job.json
```

After that you could check the result in rethinkdb web console
http://xxxxxxxxxxx.us-west-2.compute.amazonaws.com:8080/#dataexplorer


example job.json
```
{
    "target_table": "test_csv_1k.csv",
    "jobs": ["profile"],
    "data_type": "batch",
    "attributes": ["key", "a", "b", "c", "d"] ,
    "format": "hdfs"
}
```

target_table is the table name in hbase or in hdfs
jobs is a list of quality test, we currently have profile and accuracy test now
you could set format for hdfs or hbase
```
{
    "target_table": "first table name",
    "jobs": ["profile", "accuracy"],
    "data_type": "batch",
    "attributes": ["a", "b"],
    "source_table": "second table name",
    "source_id": 4,
    "format":"hbase"
}
```
### To run stream job with spark and kafka
```
example job.json
{
    "target_table": "test_topic",
    "target_id": 1,
    "jobs": ["profile"],
    "data_type": "stream",
    "attributes": ["a", "b", "c"]
}
```


## Deployment

use instruction in launcher.sh to deploy angular web app, and see the result in port 3000


## Authors
Shawn Tsai

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Technology

I built a near realtime publish subscribe application for rickshaw real-time graph

It has use these three technologies together

- https://github.com/socketio/socket.io
- https://github.com/shutterstock/rickshaw
- https://github.com/socketio/socket.io-redis

for more information check the code in 
- https://github.com/shawntsai/sdqs/blob/master/dq-client/src/app/components/monitor/monitor.component.ts
- https://github.com/shawntsai/sdqs/blob/master/dq-server/services/monitorService.js


## Purpose
1. Build batch accuracy.
2. Build stream profiling in particular time window.
3. Build batch profiling.

## future work
4. Building anomaly detection.

## Major user case

1. Many data source is not always reliable. We cannot only rely on the schemas of data sometimes the data in right format but still has many values are empty or null or the number are too bigor too small, distribution of the data may not correct, the column of the data should be distinct but not.



