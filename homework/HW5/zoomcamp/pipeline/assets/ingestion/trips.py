"""@bruin
name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default
destination: trips
with:
  - pyarrow
  - pandas
  - python-dateutil

materialization:
  type: table
  strategy: append
columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"
@bruin"""

import os
import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

def materialize():
    """
    Ingestion layer using Bruin runtime context.
    """

    # --- 1. Read Bruin date window ---
    start_date = os.environ["BRUIN_START_DATE"]  # YYYY-MM-DD
    end_date = os.environ["BRUIN_END_DATE"]

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # --- 2. Read pipeline variables ---
    vars_json = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = vars_json.get("taxi_types", ["yellow"])

    # --- 3. Generate list of (year, month) between window ---
    endpoints = []

    current = start.replace(day=1)
    end_month = end.replace(day=1)

    while current <= end_month:
        year = current.year
        month = f"{current.month:02d}"

        for taxi_type in taxi_types:
            url = (
                f"https://d37ci6vzurychx.cloudfront.net/trip-data/"
                f"{taxi_type}_tripdata_{year}-{month}.parquet"
            )
            endpoints.append(url)

        current += relativedelta(months=1)

    # --- 4. Fetch & load into DataFrames ---
    dataframes = []

    for url in endpoints:
        df = pd.read_parquet(url)
        dataframes.append(df)

    if not dataframes:
        return pd.DataFrame()

    final_dataframe = pd.concat(dataframes, ignore_index=True)

    # --- 5. Add lineage column ---
    final_dataframe["extracted_at"] = datetime.utcnow()

    return final_dataframe

