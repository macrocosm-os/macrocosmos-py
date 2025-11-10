"""
Example of using the SN13 On Demand Data Streaming service with Macrocosmos SDK.

As of the latest data-universe release:
    - Users may select two post-filtering modes via the keyword_mode parameter:
        - "any": Returns posts that contain any combination of the listed keywords.
        - "all": Returns posts that contain all of the keywords (default, if field omitted).
    - For Reddit requests, the first keyword in the list corresponds to the requested subreddit, and subsequent keywords are treated as normal.
    - For YouTube requests, only one of the following should be applied: One username (corresponding to YouTube channel name) or one keyword
      (corresponding to one YouTube video URL)
    - URL mode is mutually exclusive with `usernames` and `keywords` fields. If `url` is provided, `usernames` and `keywords` must be empty or omitted.
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
    limit=5,
    keyword_mode="any",
)

print(response)
