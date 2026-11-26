import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
load_dotenv(root / ".env")

from app.scoring import check  # noqa: E402
from app.services.llm import analyze, LLMError  # noqa: E402

GOLD = root / "data/w2/meeting_cases.json"
OUT = root / "evidence/w2/w2_eval.json"
GATE = 17  # ≥85% trên 20 case

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"same_meaning": {"type": "boolean"}},
    "required": ["same_meaning"],
    "additionalProperties": False,
}


def judge_summary(client, expected, predicted):
    # Trả về True/False, hoặc None nếu judge lỗi
    try:
        r = client.chat.completions.create(
            model=os.environ["W2_MODEL"],
            messages=[{"role": "user", "content": (
                f"Expected summary: {expected}\n"
                f"Predicted summary: {predicted}\n"
                "Does the predicted summary state the same main points as the expected summary? Answer in JSON."
            )}],
            response_format={"type": "json_schema", "json_schema": {"name": "judge", "strict": True, "schema": JUDGE_SCHEMA}},
        )
        return json.loads(r.choices[0].message.content)["same_meaning"]
    except Exception:
        return None


def main():
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_BASE_URL"],
        timeout=30.0,
        max_retries=0,
    )
    cases = json.loads(GOLD.read_text(encoding="utf-8"))
    rows, schema_ok, summary_ok_count, judge_errors = [], 0, 0, 0
    for c in cases:
        try:
            got = analyze(c["input"]).model_dump()
            schema_ok += 1
            reason = check(c["expected"], got)
            summary_ok = judge_summary(client, c["expected"]["summary"], got["summary"])
        except LLMError as e:
            got, reason, summary_ok = None, f"lỗi model: {e.kind}", False
        if summary_ok is None:
            judge_errors += 1
        if summary_ok is True:
            summary_ok_count += 1
        rows.append({
            "id": c["id"], "group": c["group"], "pass": reason == "", "reason": reason,
            "summary_ok": summary_ok, "predicted": got,
        })

    passed = sum(r["pass"] for r in rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "passed": passed, "schema_ok": schema_ok,
        "summary_ok": summary_ok_count, "judge_errors": judge_errors, "rows": rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Đạt {passed}/{len(rows)} (gate ≥{GATE}) | đúng schema {schema_ok}/{len(rows)}")
    print(f"Summary đúng nghĩa: {summary_ok_count}/{len(rows)} | judge lỗi: {judge_errors}")
    for r in rows:
        if not r["pass"]:
            print(f"  {r['id']} ({r['group']}): {r['reason']}")
    print("PASS" if passed >= GATE and schema_ok == len(rows) else "FAIL")


if __name__ == "__main__":
    main()
