# insight-project

## Project Idea

data quality is important not only in batch processing but also in streaming, I want to provide a plateform for users to do data quality test for their dataset.

## Purpose
1. Build batch accuracy.
2. Build streaming accuracy.
3. Build data profiling.
4. Building anomaly detection.

## Major user case

1. anomaly detection.
2. Many data source is not always reliable. We cannot only rely on the schemas of data sometimes the data in right format but still has many values are empty or null or the number are too bigor too small, distribution of the data may not correct, the column of the data should be distinct but not.

### Architecture
 ![alt text](https://github.com/shawntsai/insight-project/blob/master/Data%20Quality%20Diagram.png)



![alt text](https://github.com/shawntsai/insight-project/blob/master/join.png)

ubuntu@ip-10-0-0-14:~/insight-project$ /usr/local/spark/bin/spark-submit generate_simulate_data.py
number of rows: 10000
accuracy  1.0
--- 7.37636089325 seconds ---
number of rows: 100000
accuracy  1.0
--- 3.09207892418 seconds ---
number of rows: 10000000
accuracy  1.0
--- 58.5976111889 seconds ---
------------------------------------------------------------------------------------------------------
number of repeated times: 1
accuracy  1.0
--- 12.6373000145 seconds ---
number of repeated times: 10
accuracy  1.0
--- 8.45805907249 seconds ---
number of repeated times: 50
accuracy  1.0
--- 7.23118710518 seconds ---
