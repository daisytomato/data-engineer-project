# HW3

## Q1
Change the bucket name in the script, and run the python file, will automatically upload parquet file into the bucket. 

create an external table and a materialized table using the following sql command
```sql
CREATE OR REPLACE EXTERNAL TABLE `ny_taxi.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://my_ny_trip_data/yellow_tripdata_2024-*.parquet']
);

CREATE OR REPLACE TABLE `ny_taxi.yellow_taxi_2024`
AS
SELECT *
FROM `ny_taxi.external_yellow_tripdata`;
```
```sql
select count(*) from ny_taxi.external_yellow_tripdata;
```
the statement returns 20332093

## Q2
by running the two statement below and check the job information, we can get 0b for materialized table, and 155.12 mb for the other query. it is 155.12 MB for selecting one column, while the other query returns 310.24mb, doubled the estimated data processed.
```sql
select PULocationID from ny_taxi.yellow_taxi_2024
select  PULocationID , DOLocationID from ny_taxi.yellow_taxi_2024
```

## Q3

first one. as they are column stored and will take doubled time to process the data.


## Q4
```sql
select count(*) from ny_taxi.yellow_taxi_2024
where fare_amount =0;
```
the query returns 8333.

## Q5
select first and create a new table using parition and cluster
```sql
CREATE OR REPLACE TABLE `ny_taxi.clustered_yellow_trip_data`
partition by date(tpep_dropoff_datetime)
cluster by VendorID
as select * from `ny_taxi.external_yellow_tripdata`;
```

## Q6
```SQL
select distinct VendorID from ny_taxi.yellow_taxi_2024
where date(tpep_dropoff_datetime )
between date('2024-03-01') and date('2024-03-15') ;
```
Processed data  is 310.24mb.
while the query above only processed 26.84MB


## Q7
data is still store on GCP

## Q8 
False, as when table is small or when there are distinct IDs in the table, there is no need to create clusters.


## Q9
it is 0b, because i ran this query before, and it is cached. 





