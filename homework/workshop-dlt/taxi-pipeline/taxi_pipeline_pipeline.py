# ...existing code...
"""REST API dlt pipeline for NYC taxi data (paginated)."""

import requests
from typing import Iterator, Any, Dict, Optional

import dlt

BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
PAGE_SIZE = 1000


@dlt.source
def taxi_api_source(access_token: Optional[str] = dlt.secrets.value, endpoint: str = "taxi") -> Iterator:
    """
    dlt source that pages through the NYC taxi API.

    Parameters
    - access_token: optional bearer token (read from .dlt/secrets.toml by default)
    - endpoint: endpoint path under BASE_URL (default "taxi"). Adjust if the API uses a different path.
    """
    session = requests.Session()
    

    @dlt.resource(name="taxi_rides")
    def taxi_rides() -> Iterator[Dict[str, Any]]:
        page = 1
        while True:
            params = {"page": page, "per_page": PAGE_SIZE}
            url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
            resp = session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            payload = resp.json()

            # determine where records live
            if payload is None:
                break
            if isinstance(payload, dict):
                # common keys: "data", "results", "items"
                for key in ("data", "results", "items"):
                    if key in payload:
                        records = payload[key]
                        break
                else:
                    # maybe dict of single record -> treat as one record
                    records = payload
            else:
                # payload is likely a list
                records = payload

            # normalize to list
            if records is None:
                break
            if isinstance(records, dict):
                # single record -> yield and stop
                yield records
                break
            if not isinstance(records, list) or len(records) == 0:
                # stop when empty page returned
                break

            for rec in records:
                yield rec

            # stop when fewer than page size returned
            if len(records) < PAGE_SIZE:
                break
            page += 1

    # yield the resource
    yield from taxi_rides()


pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="nyc_taxi",
    refresh="drop_sources",
    progress="log",
)


if __name__ == "__main__":
    # run the pipeline against the default endpoint ("taxi"); adjust `endpoint` as needed
    load_info = pipeline.run(taxi_api_source())
    print(load_info)
# ...existing code..."""Template for building a `dlt` pipeline to ingest data from a REST API."""

