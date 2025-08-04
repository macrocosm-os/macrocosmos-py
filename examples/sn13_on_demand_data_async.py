"""
Example demonstrating concurrent async operations with the SN13 On Demand Data service.
Shows how multiple requests can be processed simultaneously in an async context.

As of data-universe release v1.9.75:
    - All keywords in the OnDemandData request will be present in the returned post/comment data.
    - For Reddit requests, the first keyword in the list corresponds to the requested subreddit, and subsequent keywords are treated as normal.
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
    request_id: int,
):
    """Fetch data for a single request and track its timing. Keep time range fixed for simplicity."""
    start_time = time.time()
    print(f"Starting request {request_id}...")

    response = await client.sn13.OnDemandData(
        source=source,
        usernames=usernames,
        keywords=keywords,
        start_date="2024-04-01",
        end_date="2025-04-25",
        limit=3,
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

    # Define multiple concurrent requests
    requests = [
        {
            "source": "x",
            "usernames": ["nasa", "spacex"],
            "keywords": ["photo", "space", "mars"],
            "request_id": 1,
        },
        {
            "source": "x",
            "usernames": ["elonmusk", "jeffbezos"],
            "keywords": ["rocket", "launch", "space"],
            "request_id": 2,
        },
        {
            "source": "reddit",
            "usernames": ["ISS", "ESA"],
            "keywords": ["r/space", "universe"],
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
