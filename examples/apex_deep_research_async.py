"""
Example of using the Apex DeepResearch API asynchronously with Macrocosmos SDK.
"""

import asyncio
import os

import macrocosmos as mc

async def demo_deep_research_async():
    """Demo asynchronous deep research job creation and status checking."""
    print("\nRunning asynchronous Deep Research example...")

    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

    client = mc.AsyncApexClient(api_key=api_key, app_name="examples/apex_deep_research")

    # Create a deep research job
    response = await client.deep_research.create_job(
        messages=[{
            "role": "user",
            "content": "Can you propose a mechanism by which a decentralized network of AI agents could achieve provable alignment on abstract ethical principles without relying on human-defined ontologies or centralized arbitration?"
        }],
        stream=True,
        task="InferenceTask",
        mixture=False,
        inference_mode="Chain-of-Thought",
        timeout=2100,
        sampling_parameters={
            "temperature": 0.7,
            "top_p": 0.95,
            "max_new_tokens": 8192,
            "do_sample": False
        }
    )

    print("\nCreated deep research job.\n")
    print(f"Initial status: {response.status}")
    print(f"Job ID: {response.job_id}")
    print(f"Created at: {response.created_at}\n")

    # Poll for job status
    while True:
        response = await client.deep_research.get_job_results(response.job_id)
        print(f"Current status: {response.status}")
        print(f"Results: {response.result}\n")
        
        if response.status == "completed":
            print("\nDeep Research Results:")
            print(response.result)
            break
        elif response.status == "failed":
            print(f"Deep research job failed: {response.error}")
            break
            
        await asyncio.sleep(20)  # Wait 20 seconds before checking again


if __name__ == "__main__":
    asyncio.run(demo_deep_research_async()) 