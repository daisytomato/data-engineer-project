/* @bruin


name: reports.trips_report


type: duckdb.sql

# TODO: Declare dependency on the staging asset(s) this report reads from.
depends:
  - staging.trips


materialization:
  type: table
  

columns:
  - name: trip_date
    type: date
    primary_key: true
  - name: taxi_type
    type: string
    primary_key: true
  - name: payment_type
    type: string
    primary_key: true
  - name: trip_count
    type: bigint
    checks:
      - name: non_negative
  - name: pickup_datetime
    type: timestamp
    checks:
      - accepted_values: not_null
@bruin */

SELECT
    CAST(pickup_datetime AS DATE) AS trip_date,
    taxi_type,
    payment_type_name AS payment_type,
    COUNT(*) AS trip_count,
    SUM(fare_amount) AS total_fare,
    AVG(fare_amount) AS avg_fare
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
GROUP BY 1, 2, 3
