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
What proportion of trips are paid with credit card?
```sql
SELECT
  payment_type,COUNT(*) AS category_count,
  (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()) AS percentage_of_total
FROM "taxi_rides"
group by 1
```
26.66%

## Q3
```sql
SELECT
  SUM(tip_amt)
 
FROM "taxi_rides"
```
answer is 6063.41