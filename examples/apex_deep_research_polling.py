"""
Example of using the Apex DeepResearch API asynchronously with Macrocosmos SDK.
Demonstrates how a deep researcher job can be polled at regular intervals
to check its current status and retrieve the latest results generated.
"""

import asyncio
import os
import json
from typing import Optional, Any, List

import macrocosmos as mc


def extract_content_from_chunk(chunk_str: str) -> Optional[str]:
    """Extract content from a JSON chunk string if available."""
    try:
        chunk_list = json.loads(chunk_str)
        if chunk_list and len(chunk_list) > 0 and "content" in chunk_list[0]:
            return chunk_list[0]["content"]
    except (json.JSONDecodeError, IndexError, KeyError) as e:
        print(f"Failed to parse chunk: {e}")
    return None


async def process_result_chunks(results: List[Any], last_seq_id: int) -> int:
    """Process result chunks and return the new last sequence ID."""
    for item in results:
        try:
            seq_id = int(item.seq_id)
            if seq_id > last_seq_id:
                if content := extract_content_from_chunk(item.chunk):
                    print(f"\nseq_id {seq_id}:\n{content}")
                    last_seq_id = seq_id
        except (ValueError, AttributeError) as e:
            print(f"Error processing sequence: {e}")
    return last_seq_id


async def demo_deep_research_polling():
    """Demo asynchronous deep research job creation and update polling."""
    print("\nRunning asynchronous Deep Research example...")

    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

    client = mc.AsyncApexClient(
        api_key=api_key, app_name="examples/apex_deep_research_polling.py"
    )

    # Create a deep research job with create_job
    submitted_response = await client.deep_research.create_job(
        messages=[
            {
                "role": "user",
                "content": """Can you propose a mechanism by which a decentralized network 
                of AI agents could achieve provable alignment on abstract ethical principles 
                without relying on human-defined ontologies or centralized arbitration?""",
            }
        ]
    )

    print("\nCreated deep research job.\n")
    print(f"Initial status: {submitted_response.status}")
    print(f"Job ID: {submitted_response.job_id}")
    print(f"Created at: {submitted_response.created_at}\n")

    # Poll for job status with get_job_results based on the job_id
    print("Polling the results...")
    last_seq_id = -1  # Track the highest sequence ID we've seen
    last_updated = None  # Track the last update time
    while True:
        try:
            polled_response = await client.deep_research.get_job_results(
                submitted_response.job_id
            )
            current_status = polled_response.status
            current_updated = polled_response.updated_at

            # On completion, print the final answer and its sequence ID
            if current_status == "completed":
                print("\nJob completed successfully!")
                print(f"\nLast update at: {current_updated}")
                if polled_response.result:
                    if content := extract_content_from_chunk(
                        polled_response.result[-1].chunk
                    ):
                        print(
                            f"\nFinal answer (seq_id {polled_response.result[-1].seq_id}):\n{content}"
                        )
                break

            elif current_status == "failed":
                print(
                    f"\nJob failed: {polled_response.error if hasattr(polled_response, 'error') else 'Unknown error'}"
                )
                print(f"\nLast update at: {current_updated}")
                break

            # Check if we have new content by comparing update times
            if current_updated != last_updated:
                print(f"\nNew update at {current_updated}")
                print(f"Status: {current_status}")

                # Process new content
                if polled_response.result:
                    last_seq_id = await process_result_chunks(
                        polled_response.result, last_seq_id
                    )
                else:
                    print(
                        "No results available yet. Waiting for Deep Researcher to generate data..."
                    )
                last_updated = current_updated

        except Exception as e:
            print(f"Error during polling: {e}")

        await asyncio.sleep(20)  # Poll in 20 second intervals


if __name__ == "__main__":
    asyncio.run(demo_deep_research_polling())
