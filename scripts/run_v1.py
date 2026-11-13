"""Chạy một file prompt trên đủ 20 case trong gold set.
Mỗi case là 1 request riêng.

Không truyền tham số thì dùng prompts/w1/v1.md và ghi evidence/w1/w1_predictions.csv.
Có tham số thì:
  python scripts/run_v1.py prompts/w1/v2.md evidence/w1/w1_predictions_v2.csv
"""
import csv
import json
import os
import sys
from pathlib import Path

from openai import OpenAI
from pydantic import ValidationError

# Dùng lại hàm classify và class IssueLabel từ classify_one.py
from classify_one import IssueLabel, classify, root


def predict(client, model, template, text):
    # Thay {issue_text} bằng nội dung issue rồi gọi model
    prompt = template.replace("{issue_text}", text)

    # Thử tối đa 2 lần. Nếu JSON không đúng khuôn thì thử lại.
    for attempt in (1, 2):
        raw = classify(client, model, prompt)
        try:
            return IssueLabel.model_validate_json(raw)
        except ValidationError:
            print(f"  attempt {attempt} schema fail")

    # Cả 2 lần đều sai khuôn thì trả về None
    return None


def path_in_repo(text):
    # Đường dẫn tương đối được tính từ thư mục gốc repo
    path = Path(text)
    if not path.is_absolute():
        path = root / path
    return path


def main():
    # 0 tham số: chạy V1 như cũ. 2 tham số: file prompt và file CSV.
    if len(sys.argv) == 1:
        prompt_path = root / "prompts/w1/v1.md"
        out_path = root / "evidence/w1/w1_predictions.csv"
    elif len(sys.argv) == 3:
        prompt_path = path_in_repo(sys.argv[1])
        out_path = path_in_repo(sys.argv[2])
    else:
        sys.exit("Usage: python scripts/run_v1.py [prompt.md output.csv]")

    cases = json.loads((root / "data/evaluation/issue_classification_gold.json").read_text())
    template = prompt_path.read_text()
    client = OpenAI(timeout=60)
    model = os.environ["OPENAI_MODEL"]

    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["issue_id", "predicted_category", "predicted_priority"])

        for case in cases:
            print(f"{case['issue_id']} ...", end=" ")
            label = predict(client, model, template, case["text"])

            if label is None:
                # Sai khuôn 2 lần: ghi INVALID để bộ chấm tính là sai
                writer.writerow([case["issue_id"], "INVALID", "INVALID"])
                print("INVALID")
            else:
                writer.writerow([case["issue_id"], label.category, label.priority])
                print(label.category, label.priority)

    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()

# V1: .venv/bin/python scripts/run_v1.py
# V2: .venv/bin/python scripts/run_v1.py prompts/w1/v2.md evidence/w1/w1_predictions_v2.csv
# Chấm: .venv/bin/python scripts/evaluate_issue_classifier.py evidence/w1/w1_predictions_v2.csv
