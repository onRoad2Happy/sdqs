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
