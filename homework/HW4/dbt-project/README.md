Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [dbt community](https://getdbt.com/community) to learn from other analytics engineers
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


# Homework
## Q1 
after run the command, the command returns 
'1 of 1 START sql view model dev.int_trips_unioned .............................. [RUN]'
Thus only this model is run

## Q2
it will fail the test as 6 is no acceptable.


## Q3 
12184
```sql
select
	count(*)
from taxi_rides_ny.dev.fact_monthly_revenue
```

## Q4
East Harlem North
```sql
select pickup_zone 
from taxi_rides_ny.dev.fact_monthly_revenue 
where service_type='Green' and year(revenue_month)=2020
group by pickup_zone
order by sum(revenue_monthly_total_amount) desc
```

## Q5
it returns 387006. 
```sql
select SERVICE_TYPE,YEAR(REVENUE_MONTH),MONTH(REVENUE_MONTH),SUM(total_monthly_trips)
from taxi_rides_ny.dev.fact_monthly_revenue 
where service_type='Green' and year(revenue_month)=2019
AND MONTH(revenue_month)=10
GROUP BY 1,2,3
```

## Q6
doing the following step:
a. downlaod 2019 data from the website.
b. insert data into duckdb.
c. create a staging model in stage folder and add the table name in the source.yml
d. dbt run --select stg_fhv_tripdata
e. ~/.duckdb/cli/latest/duckdb taxi_rides_ny.duckdb --ui
d. run the sql query to get the data. 
```sql
select count(*) from taxi_rides_ny.dev.stg_fhv_tripdata
```
43,244,693

