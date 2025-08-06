"""
Example demonstrating concurrent async operations with the SN13 On Demand Data service.
Shows how multiple requests can be processed simultaneously in an async context.

As of data-universe release v1.9.8:
    - All keywords in the OnDemandData request will be present in the returned post/comment data.
    - For Reddit requests, the first keyword in the list corresponds to the requested subreddit, and subsequent keywords are treated as normal.
    - For YouTube requests, only one username should be supplied - corresponding to the channel name - while keywords are ignored (empty list).
"""

import os
import asyncio
import time

import macrocosmos as mc


async def fetch_data(
    client: mc.AsyncSn13Client,
    source: str,
    usernames: list,
    keywords: list,
    start_date: str,
    end_date: str,
    limit: int,
    request_id: int,
):
    """Fetch data for a single request and track its timing."""
    start_time = time.time()
    print(f"Starting request {request_id}...")

    response = await client.sn13.OnDemandData(
        source=source,
        usernames=usernames,
        keywords=keywords,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )

    end_time = time.time()
    print(f"Request {request_id} completed in {end_time - start_time:.2f} seconds")
    return response


async def main():
    # Get API key from environment variables
    api_key = os.environ.get("SN13_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

    # Create async sn13 client
    client = mc.AsyncSn13Client(
        api_key=api_key, app_name="examples/sn13_on_demand_data_async.py"
    )

    # Define multiple concurrent requests with different parameters
    requests = [
        {
            "source": "x",
            "usernames": ["nasa", "spacex"],
            "keywords": ["photo", "space"],      # Posts including both keywords will be returned
            "start_date": "2024-04-01",
            "end_date": "2024-04-30",
            "limit": 5,
            "request_id": 1,
        },
        {
            "source": "reddit",
            "usernames": ["TheMuseumOfScience"],
            "keywords": ["r/nasa", "vision"],      # First keyword is the subreddit
            "start_date": "2025-04-01",
            "end_date": "2025-08-25",
            "limit": 1,
            "request_id": 2,
        },
        {
            "source": "youtube",
            "usernames": ["veritasium"],
            "keywords": [],             # YouTube does not currently support keywords, list left empty
            "start_date": "2025-08-01",
            "end_date": "2025-08-06",
            "limit": 1,
            "request_id": 3,
        },
    ]

    print("Starting concurrent requests...")
    start_time = time.time()

    # Create tasks for all requests
    tasks = [fetch_data(client, **request) for request in requests]

    # Wait for all requests to complete
    responses = await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"\nAll requests completed in {end_time - start_time:.2f} seconds")

    # Print summary of responses
    for i, response in enumerate(responses, 1):
        print("\n--------------------------------")
        print(f"\nResponse {i}:")
        print(f"Status: {response.get('status', 'unknown')}")
        print(f"Number of results: {len(response.get('data', []))}")
        print(f"Data: {response.get('data', [])}")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
