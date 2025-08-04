"""
Example of using the SN13 On Demand Data Streaming service with Macrocosmos SDK.

As of data-universe release v1.9.75:
    - All keywords in the OnDemandData request will be present in the returned post/comment data.
    - For Reddit requests, the first keyword in the list corresponds to the requested subreddit, and subsequent keywords are treated as normal.
"""

import os

import macrocosmos as mc

api_key = os.environ.get("SN13_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

client = mc.Sn13Client(api_key=api_key, app_name="examples/sn13_on_demand_data.py")

response = client.sn13.OnDemandData(
    source="x",
    usernames=["nasa", "spacex"],
    keywords=["photo", "space", "mars"],
    start_date="2024-04-01",
    end_date="2025-04-25",
    limit=3,
)

print(response)
