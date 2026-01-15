
import pandas as pd
import requests
import io
from sqlalchemy import create_engine


url ='https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'

engine =create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')
engine.connect()

df=pd.read_parquet(url)
df.to_sql('green_taxi', engine, if_exists='replace', index=False)


