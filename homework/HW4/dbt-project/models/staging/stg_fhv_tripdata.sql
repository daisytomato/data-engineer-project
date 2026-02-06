--Filter out records where dispatching_base_num IS NULL
--Rename fields to match your project's naming conventions (e.g., PUlocationID → pickup_location_id)


select 
dispatching_base_num,
pickup_datetime,
dropOff_datetime,
PUlocationID as pick_up_location_id,
DOlocationID as dropoff_location_id,
SR_Flag,
Affiliated_base_number

from {{source("raw_data", "fhv_tripdata")}}
where dispatching_base_num is not null


