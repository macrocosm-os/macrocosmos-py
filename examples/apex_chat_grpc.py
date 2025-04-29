"""
NOTE: This demo is showing how the raw gRPC endpoint works using the protobufs.

This is not recommended for most use cases, as the macrocosmos client handles
compression, retries, and other details for you.  You should use the client
interface instead.  See the other examples for how to use the client.
"""

import os

import grpc

from macrocosmos import __package_name__, __version__
from macrocosmos.resources._client import DEFAULT_BASE_URL
from macrocosmos.generated.apex.v1 import apex_pb2, apex_pb2_grpc


def demo_chat_completion():
    """Demo processing a single chat completion using the raw gRPC API."""

    channel = grpc.secure_channel(DEFAULT_BASE_URL, grpc.ssl_channel_credentials())
    stub = apex_pb2_grpc.ApexServiceStub(channel)

    messages = [apex_pb2.ChatMessage(role="user", content="Hello, how are you today?")]

    sampling_params = apex_pb2.SamplingParameters(
        temperature=0.7,
        top_p=0.9,
        max_new_tokens=256,
        do_sample=True,
    )

    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))
    metadata = [
        ("x-source", "examples/apex_chat_grpc"),
        ("x-client-id", __package_name__),
        ("x-client-version", __version__),
        ("authorization", f"Bearer {api_key}"),
    ]

    request = apex_pb2.ChatCompletionRequest(
        messages=messages,
        sampling_parameters=sampling_params,
        stream=False,
    )

    try:
        response = stub.ChatCompletion(
            request,
            metadata=metadata,
            timeout=30.0,
            compression=grpc.Compression.Gzip,
        )

        print("Response received:")
        print(f"ID: {response.id}")

        for i, choice in enumerate(response.choices):
            print(f"\nChoice {i}:")
            print(f"  Finish reason: {choice.finish_reason}")
            print(f"  Message content: {choice.message.content}")
            if choice.message.refusal:
                print(f"  Refusal: {choice.message.refusal}")

    except grpc.RpcError as e:
        print(f"RPC error: {e.code()}: {e.details()}")


def demo_chat_completion_stream():
    """Demo processing a chat completion stream using the raw gRPC API."""

    channel = grpc.secure_channel(DEFAULT_BASE_URL, grpc.ssl_channel_credentials())
    stub = apex_pb2_grpc.ApexServiceStub(channel)

    sampling_params = apex_pb2.SamplingParameters(
        temperature=0.7,
        top_p=0.9,
        max_new_tokens=256,
        do_sample=True,
    )

    messages = [
        apex_pb2.ChatMessage(
            role="user",
            content="Write a short story about a cosmonaut learning to paint.",
        )
    ]

    request = apex_pb2.ChatCompletionRequest(
        messages=messages,
        sampling_parameters=sampling_params,
        stream=True,
    )

    api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))
    metadata = [
        ("x-client-id", __package_name__),
        ("x-client-version", __version__),
        ("authorization", f"Bearer {api_key}"),
    ]

    try:
        response_stream = stub.ChatCompletionStream(
            request,
            metadata=metadata,
            timeout=30.0,
        )

        print("Streaming response:")
        full_content = ""

        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_content += content
                print(content, end="", flush=True)

    except grpc.RpcError as e:
        print(f"RPC error: {e.code()}: {e.details()}")


if __name__ == "__main__":
    print("Testing non-streaming ChatCompletion:")
    demo_chat_completion()

    print("\n" + "=" * 50 + "\n")

    print("Testing streaming ChatCompletion:")
    demo_chat_completion_stream()
