# HOMEWORK 5
## Q1
by running bruin init zoomcamp, we can see the necessary files. 
bruin.yml and pipeline/ with pipeline.yml and assets/

## Q2
adding 
materialization:
  type: table
  mode: incremental
  incremental_key: pickup_datetime
and run successfully, thus choose time_interval - incremental based on a time column

## Q3
after running bruin run --var 'taxi_types=["yellow"]', the pipeline succedeed.

## Q4
After running the following command, it worked. bruin run ingestion/trips.py --downstream

## Q5
columns:
  - name: pickup_datetime
    type: timestamp
    primary_key: true
    checks:
      - name: not_null
      - not_null: true

## Q6
run bruin lineage will give the graph 

## Q7
only bruin lineage pipeline/assets/reports/trips_report.sql is a valid command

## Q8
use full-refresh to ensure tables are created.
