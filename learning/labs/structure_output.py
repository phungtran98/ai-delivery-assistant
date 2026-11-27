from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from pydantic import BaseModel

load_dotenv()
MODEL = os.getenv("OPENAI_MODEL")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)


# 1. Định nghĩa Schema
class Person(BaseModel):
    name: str
    age: int
    job: str

# 2. Gửi request cho AI
response = client.responses.parse(
    model=MODEL,
    instructions="Trích xuất thông tin cá nhân.",
    input="Nguyễn Văn An, 22 tuổi, là lập trình viên.",
    text_format=Person
)

# 3. Nhận dữ liệu có cấu trúc
person = response.output_parsed

# 4. Hiển thị kết quả
if person is not None:
    print("Name:", person.name)
    print("Age:", person.age)
    print("Job:", person.job)
else:
    print("Không nhận được dữ liệu.")