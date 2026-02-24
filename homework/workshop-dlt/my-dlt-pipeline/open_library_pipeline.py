"""Template for building a `dlt` pipeline to ingest data from a REST API."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def open_library_rest_api_source(query: str = "harry potter") -> RESTAPIConfig:
    return rest_api_resources({
        "client":{
            "base_url": "https://openlibrary.org",
        },
        "resources":[
            {
                "name": "works_search",
                "endpoint": {
                    "path": "search.json",
                    "params": {
                        "q": query,
                        "fields": "title,author_name,first_publish_year,key",
                        "page": 1,
                    },
                    "data_selector": "docs",
                },
                # good practice to define primary key
                "primary_key": "key",
            },
        ],
    })


pipeline = dlt.pipeline(
    pipeline_name="open_library_pipeline",
    destination="duckdb",
    dataset_name="open_library_data",
    refresh="drop_sources",
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(
        open_library_rest_api_source(query="open library")
    )
    print(load_info)
