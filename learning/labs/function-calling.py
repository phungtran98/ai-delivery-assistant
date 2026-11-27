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

# 1. Tự định nghĩa hàm Python
def get_price(product):
    prices = {
        "laptop": 15000000,
        "phone": 8000000
    }
    return prices.get(product.lower(), "Không tìm thấy")


# 2. Khai báo Tools cho AI
tools = [
    {
        "type": "function",
        "name": "get_price",
        "description": "Tra cứu giá sản phẩm bằng VND",
        "parameters": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "string",
                    "description": "Tên sản phẩm"
                }
            },
            "required": ["product"],
            "additionalProperties": False
        },
        "strict": True
    }
]

# 3. Gửi yêu cầu cho AI
response = client.responses.create(
    model="gpt-6-luna",
    tools=tools,
    tool_choice="required",
    input="Laptop giá bao nhiêu?"
)

# 4. Nhận yêu cầu gọi hàm và thực thi
outputs = []

for item in response.output:
    if item.type == "function_call":
        if item.name == "get_price":
            args = json.loads(item.arguments)
            result = get_price(args["product"])

            print("Function:", item.name)
            print("Arguments:", args)
            print("Result:", result)

            outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": str(result)
            })

# 5. Gửi kết quả thực thi lại cho AI
final_response = client.responses.create(
    model="gpt-6-luna",
    previous_response_id=response.id,
    input=outputs,
    tools=tools,
    tool_choice="none"
)

print("AI Response:", final_response.output_text)
