from dataclasses import dataclass
import json
from datetime import date
import pandas as pd


@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    tip_amount: float
    passenger_count: int
    lpep_pickup_datetime : str
    lpep_dropoff_datetime: str


def ride_from_row(row):
    return Ride(
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        trip_distance=float(row['trip_distance']),
        total_amount=float(row['total_amount']),
        tip_amount=float(row['tip_amount']),
        passenger_count=int(row['passenger_count']) if not pd.isna(row['passenger_count']) else 1,
        lpep_pickup_datetime=str(row['lpep_pickup_datetime']),
        lpep_dropoff_datetime=str(row['lpep_dropoff_datetime'])
    )

# def ride_serializer(ride):
#     ride_dict = {
#         'PULocationID': ride.PULocationID,
#         'DOLocationID': ride.DOLocationID,
#         'trip_distance': ride.trip_distance,
#         'total_amount': ride.total_amount,
#         'tip_amoount': ride.tip_amoount,
#         'passenger_count': ride.passenger_count,
#         'lpep_pickup_datetime': ride.lpep_pickup_datetime,
#         'lpep_dropoff_datetime': ride.lpep_dropoff_datetime
#     }
#     json_str = json.dumps(ride_dict,default=int)
#     return json_str.encode('utf-8')

def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)