# HW7
## Q1 
```
docker exec -it hw7-redpanda-1 rpk version
```
returns 
rpk version: v25.3.9
Git ref:     836b4a36ef6d5121edbb1e68f0f673c2a8a244e2
Build date:  2026 Feb 26 07 47 54 Thu
OS/Arch:     linux/arm64
Go version:  go1.24.3

## Q2 
create a model.py and producer_green_trip.py where we define the schema of parquet file and turn the datetime columns into str
after run uv run python producer_green_trips.py, we can see the results

628.84 seconds

## Q3
create a producer file as the following and also create a consumer file which sink the data into postpres
will return 629 seconds.
uv run python Notebooks/consumer.py   
docker compose exec postgres psql -U postgres -d postgres     
then run the query which returns 8506;
```sql
select count(*) from processed_events where trip_distance > 5
```
```python
import dataclasses
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from kafka import KafkaProducer
from models import Ride, ride_from_row

# Download NYC green taxi trip data 
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"
columns = ['lpep_pickup_datetime'
,'lpep_dropoff_datetime'
,'PULocationID'
,'DOLocationID'
,'passenger_count'
,'trip_distance'
,'tip_amount'
,'total_amount']

df = pd.read_parquet(url, columns=columns)


def ride_serializer(ride):
    ride_dict = {
        'PULocationID': ride.PULocationID,
        'DOLocationID': ride.DOLocationID,
        'trip_distance': ride.trip_distance,
        'total_amount': ride.total_amount,
        'tip_amount': ride.tip_amount,
        'passenger_count': ride.passenger_count,
        'lpep_pickup_datetime': ride.lpep_pickup_datetime,
        'lpep_dropoff_datetime': ride.lpep_dropoff_datetime
    }
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=ride_serializer
)
t0 = time.time()

topic_name = 'green_trips'

for _, row in df.iterrows():
    ride = ride_from_row(row)
    producer.send(topic_name, value=ride)
    print(f"Sent: {ride}")
    time.sleep(0.01)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')
```
## Q4
modify the aggregation_job .py and create the table in postgres
```sql
SELECT PULocationID, num_trips
FROM <your_table>
ORDER BY num_trips DESC
LIMIT 3;
```
returns 74. 

## Q5
Write the results to a PostgreSQL table and find the PULocationID with the longest session (most trips in a single session).
How many trips were in the longest session?
using the same query above we get 51.


## Q6
modify the aggregation_job and run the following query;
```sql
select window_start, sum(total_tip_amount) from processed_events_aggregated_2 group by window_start  order by sum(total_tip_amount) desc limit 1;
    window_start     |  sum   
---------------------+--------
 2025-10-16 18:00:00 | 524.96
(1 row)
```
