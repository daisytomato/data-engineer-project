import io
import os
import requests
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""


# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET", " my_ny_trip_data")
path ='/Users/ethandu/Downloads/'

def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

for i in range(6):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]
        
        # csv file_name
        file_name = f"2024-{month}.parquet"
        local_file = path + 'yellow_tripdata_' + file_name
        upload_to_gcs(BUCKET, f"yellow/{file_name}",local_file)
