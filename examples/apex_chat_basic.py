"""
Example of using the Apex Chat API with Macrocosmos SDK in its most basic form.
"""

import os

import macrocosmos as mc

api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

client = mc.ApexClient(api_key=api_key, app_name="examples/apex_chat_basic")
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Write a short story about a cosmonaut learning to paint.",
        }
    ],
)

print(response)
