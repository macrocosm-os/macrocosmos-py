"""
Example of using the Apex DeepResearch API asynchronously with Macrocosmos SDK.
"""

import asyncio
import os
import json

import macrocosmos as mc


async def demo_deep_research_async():
    """Demo asynchronous deep research job creation and status checking."""
    print("\nRunning asynchronous Deep Research example...")

    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

    client = mc.AsyncApexClient(api_key=api_key, app_name="examples/apex_deep_research")

    # Create a deep research job
    submitted_response = await client.deep_research.create_job(
        messages=[
            {
                "role": "user",
                "content": "Can you propose a mechanism by which a decentralized network of AI agents could achieve provable alignment on abstract ethical principles without relying on human-defined ontologies or centralized arbitration?",
            }
        ]
    )

    print("\nCreated deep research job.\n")
    print(f"Initial status: {submitted_response['status']}")
    print(f"Job ID: {submitted_response['job_id']}")
    print(f"Created at: {submitted_response['created_at']}\n")

    # Poll for job status
    print("Polling the results...")
    last_seq_id = -1  # Track the highest sequence ID we've seen
    last_updated = None  # Track the last update time
    while True:
        try:
            polled_response = await client.deep_research.get_job_results(
                submitted_response["job_id"]
            )
            current_status = polled_response["status"]
            current_updated = polled_response["updated_at"]
            
            # Handle completion or failure first
            if current_status == "completed":
                print("\nJob completed successfully!")
                break
            elif current_status == "failed":
                print(f"\nJob failed: {polled_response.get('error', 'Unknown error')}")
                break
            
            # Check if we have new content by comparing update times
            if current_updated != last_updated:
                print(f"\nNew update at {current_updated}")
                print(f"Status: {current_status}")
                
                # Process new content
                if "result" in polled_response and polled_response["result"]:
                    for item in polled_response["result"]:
                        try:
                            seq_id = int(item["seq_id"])
                            if seq_id > last_seq_id:
                                chunk_str = item["chunk"]
                                try:
                                    chunk_list = json.loads(chunk_str)
                                    if (
                                        chunk_list
                                        and len(chunk_list) > 0
                                        and "content" in chunk_list[0]
                                    ):
                                        content = chunk_list[0]["content"]
                                        print(f"\nseq_id {seq_id}:\n{content}")
                                        last_seq_id = seq_id
                                except (
                                    json.JSONDecodeError,
                                    IndexError,
                                    KeyError,
                                ) as e:
                                    print(
                                        f"Failed to parse chunk for seq_id {seq_id}: {e}"
                                    )
                        except (ValueError, KeyError) as e:
                            print(f"Error processing sequence: {e}")
                
                last_updated = current_updated
                
        except Exception as e:
            print(f"Error during polling: {e}")

        await asyncio.sleep(20)  # Poll in 20 second intervals


if __name__ == "__main__":
    asyncio.run(demo_deep_research_async())
