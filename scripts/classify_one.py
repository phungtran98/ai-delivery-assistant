"""Chạy 1 case trong gold set.
In kết quả ra màn hình, không ghi file.

Không truyền file prompt thì dùng prompts/w1/v1.md.
Có file prompt thì:
  python scripts/classify_one.py CASE-16 prompts/w1/v3.md
"""
import json
import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

# Thư mục gốc của project (lùi 1 cấp từ thư mục scripts/)
root = Path(__file__).resolve().parents[1]

# Đọc file .env để lấy OPENAI_BASE_URL, OPENAI_MODEL, OPENAI_API_KEY
load_dotenv(root / ".env")

# Khuôn JSON mà Groq phải trả về
SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": ["Bug", "Feature", "Question", "Risk"]},
        "priority": {"type": "string", "enum": ["P1", "P2", "P3"]},
        "next_actions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["category", "priority", "next_actions"],
    "additionalProperties": False,
}


# Khuôn Pydantic để kiểm tra lại kết quả sau khi nhận về
class IssueLabel(BaseModel):
    category: Literal["Bug", "Feature", "Question", "Risk"]
    priority: Literal["P1", "P2", "P3"]
    next_actions: list[str]


def classify(client, model, prompt):
    # temperature=0 để lần chạy sau gần lần chạy trước, khi so V1/V2/V3.
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "issue_label", "strict": True, "schema": SCHEMA},
        },
    )
    # Lấy phần chữ mà model trả về
    return response.choices[0].message.content


def main():
    # 1 tham số: issue_id, prompt mặc định V1. 2 tham số: issue_id và file prompt.
    if len(sys.argv) == 2:
        issue_id = sys.argv[1]
        prompt_path = root / "prompts/w1/v1.md"
    elif len(sys.argv) == 3:
        issue_id = sys.argv[1]
        prompt_path = Path(sys.argv[2])
        if not prompt_path.is_absolute():
            prompt_path = root / prompt_path
    else:
        sys.exit("Usage: python scripts/classify_one.py CASE-01 [prompt.md]")

    # Đọc gold set
    cases = json.loads((root / "data/evaluation/issue_classification_gold.json").read_text())

    # Tìm case có issue_id trùng với tham số
    case = None
    for c in cases:
        if c["issue_id"] == issue_id:
            case = c
            break
    if case is None:
        sys.exit(f"Unknown issue_id: {issue_id}")

    # Đọc prompt và thay {issue_text} bằng nội dung issue
    if not prompt_path.is_file():
        sys.exit(f"Unknown prompt: {prompt_path}")
    prompt = prompt_path.read_text().replace("{issue_text}", case["text"])

    client = OpenAI(timeout=60)
    model = os.environ["OPENAI_MODEL"]

    # Thử tối đa 2 lần. Nếu JSON không đúng khuôn thì thử lại.
    raw = ""
    label = None
    for attempt in (1, 2):
        raw = classify(client, model, prompt)
        try:
            label = IssueLabel.model_validate_json(raw)
            break
        except ValidationError as err:
            print(f"attempt {attempt} schema fail: {err}")

    print("issue_id:", case["issue_id"])
    print("text:", case["text"])
    print("raw:", raw)
    print("parsed:", label)
    print("gold:", case["category"], case["priority"])


if __name__ == "__main__":
    main()

# V1: .venv/bin/python scripts/classify_one.py CASE-01
# V3: .venv/bin/python scripts/classify_one.py CASE-16 prompts/w1/v3.md
