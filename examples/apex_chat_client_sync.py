"""
Example of using the Apex Chat API to get multiple chat completions sequentially with the Macrocosmos SDK.
"""

import os
import time
from typing import List

import macrocosmos as mc


def demo_multiple_chat_completions():
    """Demo processing multiple chat completion requests sequentially with timing."""

    start_time_total = time.time()
    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

    message_sets = [
        [mc.ChatMessage(role="user", content="Tell me a joke about programming.")],
        [
            mc.ChatMessage(
                role="user", content="Explain quantum computing in simple terms."
            )
        ],
        [
            mc.ChatMessage(
                role="user", content="Write a haiku about artificial intelligence."
            )
        ],
        [mc.ChatMessage(role="user", content="What are the benefits of exercise?")],
    ]

    sampling_params = mc.SamplingParameters(
        temperature=0.7,
        top_p=0.9,
        max_new_tokens=50,
        do_sample=True,
    )

    client = mc.ApexClient(
        max_retries=0,
        timeout=30,
        api_key=api_key,
        app_name="examples/apex_chat_client_sync",
    )

    results = []
    for i, messages in enumerate(message_sets):
        duration = process_chat_completion(client, messages, sampling_params, i)
        results.append(duration)

    total_time = time.time() - start_time_total

    print("\n" + "=" * 50)
    print("Timing Summary:")
    for i, duration in enumerate(results):
        print(f"Request {i} completed in {duration:.2f} seconds")
    print(f"Total execution time: {total_time:.2f} seconds")
    print("=" * 50)


def process_chat_completion(
    client: mc.ApexClient,
    messages: List[mc.ChatMessage],
    sampling_params: mc.SamplingParameters,
    index: int,
):
    """Helper function to process a single chat completion request and return the duration."""
    import time

    start_time = time.time()

    try:
        print(f"\nStarting request {index} with prompt: {messages[0].content[:50]}...")

        response: mc.ChatCompletionResponse = client.chat.completions.create(
            messages=messages,
            sampling_parameters=sampling_params,
        )

        duration = time.time() - start_time

        print(f"\nResponse {index} received (took {duration:.2f}s):")
        print(f"  Content {index}: {response.choices[0].message.content[:80]}...")

        return duration

    except Exception as e:
        duration = time.time() - start_time
        print(
            f"RPC error in request {index} (after {duration:.2f}s): {e.code()}: {e.details()}"
        )
        return duration


if __name__ == "__main__":
    print("Testing multiple sequential ChatCompletions:")
    demo_multiple_chat_completions()
