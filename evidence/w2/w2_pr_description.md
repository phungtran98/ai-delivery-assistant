# W2 PR description

Copy vào GitHub PR theo `evidence/weekly_pr_template.md`.

**Member:** _(điền tên)_

**Feature:**
POST `/analyze-meeting` – trích xuất summary, decisions, action items từ biên bản họp bằng structured output; xử lý lỗi; demo UI; eval ≥17/20.

**What I studied:**
OpenAI Quickstart, Structured Outputs; validate phía server (Pydantic); timeout / 429 / upstream / bad JSON retry.

**What I built (summary + key modules):**
- `app/schemas.py`, `app/services/llm.py`, `app/main.py`, `app/scoring.py`
- `tests/test_w2_errors.py` (mock 5 kịch bản lỗi + schema)
- `scripts/evaluate_w2_meetings.py`, `app/static/demo.html` (`/demo`)
- Evidence: `evidence/w2/w2_eval.json`, `w2_walkthrough.md`, `w2_error_reasons.md`, `analyze_meeting.http`

**How to run:**
```bash
env $(grep -E "^(OPENAI_API_KEY|OPENAI_BASE_URL|W2_MODEL)=" .env | xargs) .venv/bin/uvicorn app.main:app --port 8000
.venv/bin/python -m pytest -q tests/test_w2_errors.py tests/test_mock_jira.py
.venv/bin/python scripts/evaluate_w2_meetings.py
```

**Results:**
- Schema: 20/20
- Extraction (owner + due_date + counts): **18/20** (PASS gate ≥17)
- Error tests: 6 passed; mock Jira: 3 passed; smoke: PASS
- Demo: `http://127.0.0.1:8000/demo`

**Known failures:**
- TC07, TC09: thiếu 1 decision (chi tiết `evidence/w2/w2_error_reasons.md`)
- Bộ case đang dùng là mentor public set; mục E (tự viết 20 case) chưa tách riêng
- Summary judge dao động; không tính vào gate

**Demo link:** `http://127.0.0.1:8000/demo` (+ `/docs`)

**PR link:** _(điền sau khi mở PR)_

**Next action:** video màn hình; gửi link PR cho mentor; (tuỳ chọn) bổ sung bộ case tự viết.
