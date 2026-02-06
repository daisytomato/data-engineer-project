import duckdb
import requests
from pathlib import Path


con = duckdb.connect("taxi_rides_ny.duckdb")
print("successfully connected to duckdb")
con.execute("CREATE SCHEMA IF NOT EXISTS prod")
print("Connected to DuckDB database 'taxi_rides_ny.duckdb' successfully.")
con.execute(f"""
        CREATE OR REPLACE TABLE prod.fhv_tripdata AS
        SELECT * FROM read_parquet('data/fhv/*.parquet', union_by_name=true)
    """)

con.close()