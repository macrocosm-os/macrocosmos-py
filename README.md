# Macrocosmos Python SDK

The offical Python SDK for [Macrocosmos](https://www.macrocosmos.ai/).

# Installation

```bash
pip install macrocosmos
```

# Usage

## Apex
Apex is a decentralized agentic inference engine powered by Subnet 1 on the Bittensor network.  You can read more about this subnet on the [Macrocosmos Apex page](https://www.macrocosmos.ai/sn1).

### Chat Completions
Use the synchronous `ApexClient` or asynchronous `AsyncApexClient` for inferencing tasks. See the examples for additional features and functionality.

```py
import macrocosmos as mc

client = mc.ApexClient(api_key=api_key)
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a short story about a cosmonaut learning to paint."}],
)

print(response)
```
