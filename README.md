# insight-project



## Project Idea

aws spot instance recommendation is a web application with data pipeline supporting current instances availability, recommending request spot fleet helping client to build a fault-tolerance and economical application.

## Purpose

Using different types of instaces, weighting may affect the final price, aws only support in zone evaluation of multiple instances. I want to support in stream analysis such as the deviation of prices in different zone which would affect the fault-tolerance system. And also give warning to users for those instances that currently fluctuate a lot in a reasonable hours.

## Major user case

1. user query spot instances, and application give availability 
2. user gives cpu, memory, location, show the availability instances and the estimated costs, interruption probability.
3. user only gives cpu, memory show the estimated number of instances of different type, and instance number and estimated costs by zone.
4. if user don’t care about zone, gives instances where has lowest price in particular zone
5. if current zone has not enough instances for particular user (really unlikely) suggest different zone’s instances to them
6. generate a recommendation sheet which contains instances types, average spot price, zone, interruption likelihood.
7. show product price visualization.
8. user can check his history recommendation data.
9. user browsed some sample recommendation sheet.

### Architecture
![alt text](https://github.com/shawntsai/insight-project/blob/master/architect_insight.png)
