"""
Example of using the Apex Web Search API with Macrocosmos SDK.
"""

import asyncio
import os

import macrocosmos as mc


# Synchronous example
def demo_web_search_sync():
    """Demo synchronous web search using the Macrocosmos SDK."""

    print("Running synchronous example")
    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))
    client = mc.ApexClient(api_key=api_key, app_name="examples/apex_web_search")

    # Simple web search query
    response = client.web_search.search(
        search_query="What is Bittensor?",
        max_results_per_miner=3,
        max_response_time=20,
    )

    # Print the results
    print(f"Got {len(response.results)} results for 'What is Bittensor?'")
    for i, result in enumerate(response.results):
        print(f"\nResult {i + 1}:")
        print(f"URL: {result.url}")
        print(f"Relevant content: {result.relevant[:200]}...")


# Asynchronous example
async def demo_web_search_async():
    """Demo asynchronous web search using the Macrocosmos SDK."""

    print("\nRunning asynchronous example")
    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))
    client = mc.AsyncApexClient(api_key=api_key, app_name="examples/apex_web_search")

    # Simple web search query
    response = await client.web_search.search(
        search_query="Latest AI research papers",
        max_results_per_miner=3,
        max_response_time=20,
    )

    # Print the results
    print(f"Got {len(response.results)} results for 'Latest AI research papers'")
    for i, result in enumerate(response.results):
        print(f"\nResult {i + 1}:")
        print(f"URL: {result.url}")
        print(f"Relevant content: {result.relevant[:200]}...")


if __name__ == "__main__":
    # Run synchronous example
    demo_web_search_sync()

    # Run asynchronous example using asyncio
    asyncio.run(demo_web_search_async())
