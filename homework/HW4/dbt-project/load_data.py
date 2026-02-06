import duckdb

con = duckdb.connect("taxi_rides_ny.duckdb")
print ("Connected to DuckDB database 'taxi_rides_ny.duckdb' successfully.")
con.execute("CREATE SCHEMA IF NOT EXISTS prod")
for taxi_type in ["yellow", "green"]:
    con.execute(f"""
                CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
                SELECT * FROM read_parquet('{taxi_type}_tripdata_*.parquet', union_by_name=true)
            """)
con.close()
print ('Data loaded into DuckDB successfully.')


