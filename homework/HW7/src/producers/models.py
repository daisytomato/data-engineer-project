from dataclasses import dataclass
import json


@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    tpep_pickup_datetime: int

def ride_from_row(row):
    return Ride(
        PULocationID=row['PULocationID'],
        DOLocationID=row['DOLocationID'],
        trip_distance=row['trip_distance'],
        total_amount=row['total_amount'],
        tpep_pickup_datetime=int(row['tpep_pickup_datetime'].timestamp()*1000)
    )

def ride_serializer(ride):
    ride_dict = {
        'PULocationID': ride.PULocationID,
        'DOLocationID': ride.DOLocationID,
        'trip_distance': ride.trip_distance,
        'total_amount': ride.total_amount,
        'tpep_pickup_datetime': ride.tpep_pickup_datetime
    }
    json_str = json.dumps(ride_dict,default=int)
    return json_str.encode('utf-8')

def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)