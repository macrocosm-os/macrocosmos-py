"""
Example of using the async Apex Chat API to stream a chat completion using the Macrocosmos SDK.
"""

import asyncio
import os

import macrocosmos as mc


async def demo_chat_completion_stream():
    """Demo using the chat completion stream API using the client interface."""

    messages = [
        mc.ChatMessage(
            role="user",
            content="Write a short story about a cosmonaut learning to paint.",
        )
    ]
    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

    sampling_params = mc.SamplingParameters(
        temperature=0.7,
        top_p=0.9,
        max_new_tokens=256,
        do_sample=True,
    )

    client = mc.AsyncApexClient(
        max_retries=0,
        timeout=30,
        api_key=api_key,
        app_name="examples/apex_chat_client_stream",
    )

    try:
        response_stream = await client.chat.completions.create(
            messages=messages,
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
        print(f"RPC error: {e.code()}: {e.details()}")


if __name__ == "__main__":
    print("Testing streaming ChatCompletion:")
    asyncio.run(demo_chat_completion_stream())
