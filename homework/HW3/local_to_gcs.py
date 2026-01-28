from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = " my_ny_trip_data"

    # The path to your file to upload
    for i in range(6):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # csv file_name
        file_name = f"/Users/ethandu/Downloadsyellow_tripdata_{2024}-{month}.parquet"



    # The ID of your GCS object (destination path in the bucket)
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    ##blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

# Example usage:
# upload_blob("my-great-bucket", "my_local_file.txt", "folder_name/my_remote_file.txt")
