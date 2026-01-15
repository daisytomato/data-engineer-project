#Homework 1
# Q1
```bash
#run a dokcer image
docker run -it \
--rm \
--entrypoint=bash \
python:3.13-slim
```
```bash
#get pip version
pip --version
```
# Q2
copy and paste yaml file 
specify the names , db:5433 worked

# Q3
create ingest_data.py to ingest parquet data into database
create zone_data.py to ingest csv data into database
create docker-compose.yaml file to create containers without using docker network
uv run above scripts and insert data into table
```sql
select count(#) from green_taxi 
where 1=1
and date(lpep_pickup_datetime) >= date '2025-11-01' and date(lpep_dropoff_datetime) <'2025-12-01'
and  trip_distance <=1
```
8007

# Q4
```SQL
select  date(lpep_pickup_datetime)  
from green_taxi 
where  trip_distance <100
order by trip_distance desc
limit 1
```
# Q5
```sql
select z."Zone"
from green_taxi as g
left join zone_lookup as z
on g."PULocationID" = z."LocationID"
where date("lpep_pickup_datetime") ='2025-11-18' and date("lpep_dropoff_datetime") ='2025-11-18'
group by "Zone"
order by sum(trip_distance) desc
limit 1
```
#  Q6
```SQL
select dz."Zone"
from green_taxi as g
inner join zone_lookup as pz
on g."PULocationID" = pz."LocationID"
and pz."Zone" = 'East Harlem North'
inner join zone_lookup as dz
on g."DOLocationID" = dz."LocationID"
order by tip_amount desc
limit 1
```
# Q7
first create a service account and save credentials in a json file
then export GOOGLE_APPLICATION_CREDENTIAL
THEN using main.tf
