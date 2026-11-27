import json
import sys
from pathlib import Path

from dotenv import load_dotenv

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
load_dotenv(root / ".env")

from app.scoring import check  # noqa: E402
from app.services.llm import analyze, LLMError  # noqa: E402

GOLD = root / "data/w2/meeting_cases.json"
OUT = root / "evidence/w2/w2_eval.json"
GATE = 17  # ≥85% trên 20 case


def main():
    # Chỉ analyze + check(gold). Summary judge (Gold | AI | đúng nghĩa) làm sau.
    cases = json.loads(GOLD.read_text(encoding="utf-8"))
    rows, schema_ok = [], 0
    for c in cases:
        try:
            got = analyze(c["input"]).model_dump()
            schema_ok += 1
            reason = check(c["expected"], got)
        except LLMError as e:
            got, reason = None, f"lỗi model: {e.kind}"
        rows.append({
            "id": c["id"],
            "group": c["group"],
            "pass": reason == "",
            "reason": reason,
            "summary_ok": None,  # chưa chấm; judge summary để làm sau
            "predicted": got,
        })

    passed = sum(r["pass"] for r in rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "passed": passed,
        "schema_ok": schema_ok,
        "summary_ok": None,
        "summary_judge": "deferred",
        "judge_errors": 0,
        "rows": rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Đạt {passed}/{len(rows)} (gate ≥{GATE}) | đúng schema {schema_ok}/{len(rows)}")
    print("Summary judge: chưa chạy (làm sau — Gold | AI | đúng nghĩa)")
    for r in rows:
        if not r["pass"]:
            print(f"  {r['id']} ({r['group']}): {r['reason']}")
    print("PASS" if passed >= GATE and schema_ok == len(rows) else "FAIL")


if __name__ == "__main__":
    main()
