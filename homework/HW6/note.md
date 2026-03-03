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

