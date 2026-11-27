from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

stream = client.responses.create(
    model="gpt-6-luna",
    input="Giải thích AI là gì trong 200 từ.",
    stream=True
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)

print()
