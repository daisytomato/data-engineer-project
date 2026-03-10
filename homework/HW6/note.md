## First look at pyspark 
 * Reading CSV files
    better if we use uv for each project. uv add pyspark uv add jupyter 
    !gzip -dc fhvhv_tripdata_2021-01.csv.gz > fhvhv_tripdata_2021-01.csv , if i use gzip -dc without put it into a file, it will crash
 * Partitions
    df.write.parquet() what does it do? it 
    Distributes data across partitions
    Writes multiple .parquet files
    Creates a folder (not a single file)
    Stores schema in metadata

 * Saving data to Parquet for local environments
    don't forget to uv add pandas when using jupyter . 
    integer 4 bytes
    long integer 9 bytes
    split one large file into many partitions. 
    df.repartition(14)
 * Spark Master UI
        sparkUI, localhost4040

Actions vs Transformations:
Transformation ( lazy not executed immediately):
    * selecting columns 
    * Filtering 
    * join
    * groupby
Action --eager, executed immdediately:
    * .show()
    * .take()
    * .head()
    * .write()

Test using yellow tripdata
* no space between '='
* set parameters set -e , so can run command with random value
* watch out for lower and upper case 

df_trips_data.registerTempTable('trips_data')

## Spark Cluster
 sparkdriver, master, download data from cloud storage and write the data back in the cloud storage.

 * Group by 
 first do filter and group by on partition, then group by stage #2, combine all the partition results.

 ## join
    when join two large tables, will ccreate harsh key for each record.
    when we have a table is small like zones, and another table that is big like revenue, the zones table will be broadcasted(copied) in each executor in stead of reshuffle. 
## Resilient Distributed Datasets
   map and reduece
   RDD: collection of objects
   dataframe: has schemas

   df_green.rdd (rows returned)

   map function
    row ---> map ---> ....(rdd, key = (hour,zone), value = amount), then reshuffling based on keys.

ReduceBy Key
(key,value) ----> reduce ---> (key,reduced_value)
   rdd

   k1,v1
   k1,v2   -----> v1,v2 > v1+v2 

   left_amount, left_count = left_value is valid when left_value is a tuple.
 ### map partition

 ## connecting to GCS
* download gcs via brew
* download haddop connector
* connect through config
* create a context then create a spark session

## Creating a local spark cluster
* create a local cluster
* turning the notebook into a cluster



## creating cloud cluster

 




