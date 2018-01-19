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

## compare result for number rows
1. number of rows: 10000
accuracy  1.0
--- 7.37636089325 seconds ---
2. number of rows: 100000
accuracy  1.0
--- 3.09207892418 seconds ---
3. number of rows: 10000000
accuracy  1.0
--- 58.5976111889 seconds ---

## compare result for number of repeated keys
------------------------------------------------------------------------------------------------------
1. number of repeated times: 1
 --- 12.6373000145 seconds ---
2. number of repeated times: 10
--- 8.45805907249 seconds ---
3. number of repeated times: 50
--- 7.23118710518 seconds ---



### Architecture
 ![alt text](https://github.com/shawntsai/insight-project/blob/master/Data%20Quality%20Diagram.png)
 ![alt text](https://github.com/shawntsai/insight-project/blob/master/join.png)

