"""REST API dlt pipeline for NYC taxi data (paginated)."""

import requests
from typing import Iterator, Any, Dict, Optional

import dlt

BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
PAGE_SIZE = 1000


@dlt.source
def taxi_api_source(
    access_token: Optional[str] = None,  # ✅ remove forced secret resolution
    endpoint: str = "taxi",
):

    session = requests.Session()

    # only attach auth if provided
    if access_token:
        session.headers.update({"Authorization": f"Bearer {access_token}"})

    session.headers.update({"Accept": "application/json"})

    @dlt.resource(name="taxi_rides", write_disposition="replace")
    def taxi_rides() -> Iterator[Dict[str, Any]]:
        page = 1

        while True:
            params = {"page": page, "per_page": PAGE_SIZE}
            url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

            resp = session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            payload = resp.json()

            if not payload:
                break

            if isinstance(payload, dict):
                records = (
                    payload.get("data")
                    or payload.get("results")
                    or payload.get("items")
                    or payload
                )
            else:
                records = payload

            if not isinstance(records, list) or not records:
                break

            for rec in records:
                yield rec

            if len(records) < PAGE_SIZE:
                break

            page += 1

    # ✅ IMPORTANT: return the resource, don’t yield rows
    return taxi_rides


pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="nyc_taxi",
    refresh="drop_sources",
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(taxi_api_source())
    print(load_info)