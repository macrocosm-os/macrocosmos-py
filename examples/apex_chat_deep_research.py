"""
Example of using the async Apex Chat API to stream a chat completion using the Macrocosmos SDK.
"""

import asyncio
import os
import time

import macrocosmos as mc


async def demo_deep_research():
    """Demo deep research."""

    messages = [
        mc.ChatMessage(
            role="user",
            content="How do you design a federated LLM training pipeline that shards the model across remote systems across untrusted nodes?",
        )
    ]
    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

    sampling_params = mc.SamplingParameters(
        temperature=0.6,
        top_p=0.95,
        max_new_tokens=8192,
        do_sample=False,
    )

    client = mc.AsyncApexClient(
        max_retries=0,
        timeout=21000,
        api_key=api_key,
        app_name="examples/apex_chat_deep_research",
    )

    try:
        start_time = time.time()
        response_stream = await client.chat.completions.create(
            model="mrfakename/mistral-small-3.1-24b-instruct-2503-hf",
            messages=messages,
            inference_mode="Chain-of-Thought",
            sampling_parameters=sampling_params,
            stream=True,
        )

        print("Streaming response:")
        full_content = ""

        chunk: mc.ChatCompletionChunkResponse
        async for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_content += content
                print(content, end="", flush=True)

    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise e
    finally:
        print(f"\nTotal time taken: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    print("Testing streaming ChatCompletion:")
    asyncio.run(demo_deep_research())
