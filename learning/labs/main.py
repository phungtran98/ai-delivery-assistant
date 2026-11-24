from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)




def generate_response(input_text, model=MODEL, tools=None):
    response = client.responses.create(
        model=model,
        input=input_text,
        tools=tools or [],
    )
    return response.output_text






# q1="Hãy giải thích Python là gì bằng tiếng Việt."
# t1=[]
# print(generate_response(model=MODEL, input_text=q1, tools=t1))


def run(label, text, tools):
    print("\n===", label, "===")
    try:
        print(generate_response(input_text=text, tools=tools))
    except Exception as err:
        print("ERROR:", type(err).__name__, err)


run(
    "web_search",
    "Tôi muốn tìm một tin thời sự Mỹ và Iran mới nhất hôm nay.",
    [{"type": "web_search"}],
)
run(
    "function",
    "Thời tiết Hà Nội hôm nay?",
    [{
        "type": "function",
        "name": "get_weather",
        "description": "Lấy thời tiết của một thành phố",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    }],
)
run(
    "code_interpreter",
    "Tính 17 * 23.",
    [{"type": "code_interpreter", "container": {"type": "auto"}}],
)
run(
    "file_search",
    "Tóm tắt tài liệu trong kho.",
    [{"type": "file_search", "vector_store_ids": ["vs_xxx"]}],
)