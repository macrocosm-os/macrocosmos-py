# Macrocosmos Python SDK

The offical Python SDK for [Macrocosmos](https://www.macrocosmos.ai/).

# Installation

## Using `pip`
```bash
pip install macrocosmos
```

## Using `uv`
```bash
uv add macrocosmos
```

# Usage
For a comprehensive overview of available functionality and integration patterns, refer to the [Macrocosmos SDK guide](https://docs.macrocosmos.ai/developers/macrocosmos-sdk).

## Apex
Apex is a decentralized agentic inference engine powered by Subnet 1 on the Bittensor network.  You can read more about this subnet on the [Macrocosmos Apex page](https://www.macrocosmos.ai/sn1).

Use the synchronous `ApexClient` or asynchronous `AsyncApexClient` for inferencing tasks. See the examples for additional features and functionality.

### Chat Completions
```py
import macrocosmos as mc

client = mc.ApexClient(api_key="<your-api-key>", app_name="my_app")
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a short story about a cosmonaut learning to paint."}],
)

print(response)
```

### Web Search
```py
import macrocosmos as mc

client = mc.ApexClient(api_key="<your-api-key>", app_name="my_app")
response = client.web_search.search(
    search_query="What is Bittensor?",
    max_results_per_miner=3,
    max_response_time=20,
)

print(response)
```

### Deep Researcher

#### Submit a deep researcher job

```py
import macrocosmos as mc

client = mc.ApexClient(api_key="<your-api-key>", app_name="my_app")
submitted_response = client.deep_research.create_job(
        messages=[
            {
                "role": "user",
                "content": """Can you propose a mechanism by which a decentralized network 
                of AI agents could achieve provable alignment on abstract ethical principles 
                without relying on human-defined ontologies or centralized arbitration?""",
            }
        ]
    )

print(submitted_response)
```

#### Retrieve the results of a deep researcher job

```py
import macrocosmos as mc

client = mc.ApexClient(api_key="<your-api-key>", app_name="my_app")
polled_response = client.deep_research.get_job_results(job_id="<your-job-id>")

print(polled_response)
```

## SN13 OnDemandAPI

SN13 is focused on large-scale data collection. With the OnDemandAPI, you can run precise, real-time queries against platforms like X (Twitter) and Reddit (YouTube forthcoming).

As of data-universe release [v1.9.75](https://github.com/macrocosm-os/data-universe/releases/tag/v1.9.75):
- All keywords in an OnDemandData request will be present in the returned post/comment data.
- For Reddit requests, the first keyword in the list corresponds to the requested subreddit, and subsequent keywords are treated as normal.

Use the synchronous `Sn13Client` to query historical or current data based on users, keywords, and time range.

### Query Example

```py
import macrocosmos as mc

client = mc.Sn13Client(api_key="<your-api-key>", app_name="my_app")

response = client.sn13.OnDemandData(
    source='X',                 # or 'Reddit'
    usernames=["@nasa"],        # Optional, up to 5 users
    keywords=["galaxy"],        # Optional, up to 5 keywords
    start_date='2025-04-15',    # Defaults to 24h range if not specified
    end_date='2025-05-15',      # Defaults to current time if not specified
    limit=1000                  # Optional, up to 1000 results
)

print(response)
```

## Gravity
Gravity is a decentralized data collection platform powered by Subnet 13 (Data Universe) on the Bittensor network.  You can read more about this subnet on the [Macrocosmos Data Universe page](https://www.macrocosmos.ai/sn13).

Use the synchronous `GravityClient` or asynchronous `AsyncGravityClient` for creating and monitoring data collection tasks.  See the [examples/gravity_workflow_example.py](https://github.com/macrocosm-os/macrocosmos-py/blob/main/examples/gravity_workflow_example.py) for a complete working example of a data collection CLI you can use for your next big project or to plug right into your favorite data product.

### Creating a Gravity Task for Data Collection
Gravity tasks will immediately be registered on the network for miners to start working on your job.  The job will stay registered for 7 days.  After which, it will automatically generate a dataset of the data that was collected and an email will be sent to the email address you specify.

```py
import macrocosmos as mc

client = mc.GravityClient(api_key="<your-api-key>", app_name="my_app")

gravity_tasks = [
    {"topic": "#ai", "platform": "x"},
    {"topic": "r/MachineLearning", "platform": "reddit"},
]

notification = {
    "type": "email",
    "address": "<your-email-address>",
    "redirect_url": "https://app.macrocosmos.ai/",
}

response =  client.gravity.CreateGravityTask(
    gravity_tasks=gravity_tasks, name="My First Gravity Task", notification_requests=[notification]
)

# Print the gravity task ID
print(response)
```

### Get the status of a Gravity Task and its Crawlers
If you wish to get further information about the crawlers, you can use the `include_crawlers` flag or make separate `GetCrawler()` calls since returning in bulk can be slow.

```py
import macrocosmos as mc

client = mc.GravityClient(api_key="<your-api-key>", app_name="my_app")

response = client.gravity.GetGravityTasks(gravity_task_id="<your-gravity-task-id>", include_crawlers=False)

# Print the details about the gravity task and crawler IDs
print(response)
```

### Build Dataset
If you do not want to wait 7-days for your data, you can request it earlier.  Add a notification to get notified when the build is complete or you can monitor the status by calling `GetDataset()`.  Once the dataset is built, the gravity task will be de-registered.  Calling `CancelDataset()` will cancel a build in-progress or, if it's already complete, will purge the created dataset.

```py
import macrocosmos as mc

client = mc.GravityClient(api_key="<your-api-key>", app_name="my_app")

notification = {
    "type": "email",
    "address": "<your-email-address>",
    "redirect_url": "https://app.macrocosmos.ai/",
}

response = client.gravity.BuildDataset(
    crawler_id="<your-crawler-id>", notification_requests=[notification]
)

# Print the dataset ID
print(response)
```
