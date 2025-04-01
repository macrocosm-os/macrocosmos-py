# Macrocosmos Python SDK

The offical Python SDK for [Macrocosmos](https://www.macrocosmos.ai/).

# Installation

```bash
pip install macrocosmos
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
