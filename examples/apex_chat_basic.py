import macrocosmos as mc
import os

api_key = os.environ.get("APEX_API_KEY", os.environ.get("MACROCOSMOS_API_KEY", "test_api_key"))

client = mc.ApexClient(api_key=api_key)
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a short story about a cosmonaut learning to paint."}],
)

print(response)
