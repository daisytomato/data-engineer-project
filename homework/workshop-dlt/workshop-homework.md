## Q1 
uv run dlt pipeline taxi-pipeline show
by running the query 
```sql
SELECT
  max(trip_dropoff_date_time),min(trip_dropoff_date_time)
FROM "taxi_rides"
LIMIT 1000
```
can see the date is from 2009-06-01 to 2009-07-01

## Q2
