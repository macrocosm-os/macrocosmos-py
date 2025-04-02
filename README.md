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
For complete documentation on the SDK and API, check out the [Macrocosmos guide](https://guide.macrocosmos.ai/api-documentation/introduction).

## Apex
Apex is a decentralized agentic inference engine powered by Subnet 1 on the Bittensor network.  You can read more about this subnet on the [Macrocosmos Apex page](https://www.macrocosmos.ai/sn1).

Use the synchronous `ApexClient` or asynchronous `AsyncApexClient` for inferencing tasks. See the examples for additional features and functionality.

### Chat Completions
```py
import macrocosmos as mc

client = mc.ApexClient(api_key="<your-api-key>")
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a short story about a cosmonaut learning to paint."}],
)

print(response)
```

### Web Search
```py
import macrocosmos as mc

client = mc.ApexClient(api_key="<your-api-key>")
response = client.web_search.search(
    search_query="What is Bittensor?",
    n_results=3,
    max_response_time=20,
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

client = mc.GravityClient(api_key="<your-api-key>")

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

client = mc.GravityClient(api_key="<your-api-key>")

response = client.gravity.GetGravityTasks(gravity_task_id="<your-gravity-task-id>", include_crawlers=False)

# Print the details about the gravity task and crawler IDs
print(response)
```

### Build Dataset
If you do not want to wait 7-days for your data, you can request it earlier.  Add a notification to get notified when the build is complete or you can monitor the status by calling `GetDataset()`.  Once the dataset is built, the gravity task will be de-registered.  Calling `CancelDataset()` will cancel a build in-progress or, if it's already complete, will purge the created dataset.

```py
import macrocosmos as mc

client = mc.GravityClient(api_key="<your-api-key>")

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
