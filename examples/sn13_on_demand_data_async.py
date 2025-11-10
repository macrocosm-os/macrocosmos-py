"""
Example demonstrating concurrent async operations with the SN13 On Demand Data service.
Shows how multiple requests can be processed simultaneously in an async context.

As of the latest data-universe release:
    - Users may select two post-filtering modes via the keyword_mode parameter:
        - "any": Returns posts that contain any combination of the listed keywords.
        - "all": Returns posts that contain all of the keywords (default, if field omitted).
    - For Reddit requests, the first keyword in the list corresponds to the requested subreddit, and subsequent keywords are treated as normal.
    - For YouTube requests, only one of the following should be applied: One username (corresponding to YouTube channel name) or one keyword
      (corresponding to one YouTube video URL).
    - URL mode is mutually exclusive with `usernames` and `keywords` fields. If `url` is provided, `usernames` and `keywords` must be empty or omitted.
"""

import os
import asyncio
import time
from typing import Optional

import macrocosmos as mc


async def fetch_data(
    client: mc.AsyncSn13Client,
    source: str,
    start_date: str,
    end_date: str,
    limit: int,
    request_id: int,
    keyword_mode: Optional[str] = None,
    url: Optional[str] = None,
    keywords: Optional[list] = None,
    usernames: Optional[list] = None,
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
        keyword_mode=keyword_mode,
        url=url,
    )

    end_time = time.time()
    print(f"\nRequest {request_id} completed in {end_time - start_time:.2f} seconds")
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
            "keywords": [
                "photo",
                "space",
            ],  # Posts including either keyword will be returned
            "start_date": "2024-04-01",
            "end_date": "2024-04-28",
            "limit": 5,
            "request_id": 1,
            "keyword_mode": "any",
        },
        {
            "source": "reddit",
            "keywords": [
                "r/nasa",
                "satellites",
                "recover",
            ],  # First keyword is the subreddit, next keywords should all appear in returned posts
            "start_date": "2025-10-01",
            "end_date": "2025-10-06",
            "limit": 1,
            "request_id": 2,
            "keyword_mode": "all",
        },
        {
            "source": "youtube",
            "usernames": ["veritasium"],  # single username/channel is provided
            "start_date": "2025-07-01",
            "end_date": "2025-09-04",
            "limit": 1,
            "request_id": 3,
        },
        {
            "source": "youtube",
            "url": "https://www.youtube.com/watch?v=fnjIoWh7yAc",
            "start_date": "2025-07-01",
            "end_date": "2025-09-04",
            "limit": 1,
            "request_id": 4,
        },
        {
            "source": "x",
            "url": "https://x.com/MacrocosmosAI/status/1928491993338167573",
            "start_date": "2025-01-01T00:00:00Z",
            "end_date": "2025-10-31T23:59:57Z",
            "limit": 1,
            "request_id": 5,
        },
    ]

    print("Starting concurrent requests...")
    start_time = time.time()

    # Create tasks for all requests
    tasks = [fetch_data(client, **request) for request in requests]

    # Stream results as each request completes
    completed = 0
    for coro in asyncio.as_completed(tasks):
        try:
            response = await coro
            completed += 1
            elapsed = time.time() - start_time
            print(f"\n[{completed}/{len(tasks)}] completed at {elapsed:.2f} seconds")
            print("\n--------------------------------")
            print(f"\nResponse {completed}:")
            print(f"Status: {response.get('status', 'unknown')}")
            print(f"Number of results: {len(response.get('data', []))}")
            print(f"Data: {response.get('data', [])}")
        except Exception as e:
            completed += 1
            elapsed = time.time() - start_time
            print(f"\n[{completed}/{len(tasks)}] failed at {elapsed:.2f} seconds: {e}")

    end_time = time.time()
    print(f"\nAll requests completed in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
