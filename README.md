# AI Engineering Fast-Track V12 – Member Starter Kit

Companion to `TMA_AI_Engineering_Fast_Track_Member_Package_v12_Self_Learning_Ready.pptx`.
This kit provides **real synthetic fixtures and reusable local tools**; it intentionally does **not** include completed assignment solutions.

## Quick start (macOS / Linux / Windows PowerShell equivalent)
1. Install **Python 3.11+**, Git and Docker; use an isolated training environment.
2. `python -m venv .venv` then activate the environment.
3. `pip install -r requirements.txt`.
4. `python scripts/smoke_test.py` — expected output ends with **PASS**.
5. `pytest -q tests/test_mock_jira.py` — expected **3 passed**.
6. `uvicorn app.mock_jira:app --reload --port 8001`; visit `http://127.0.0.1:8001/docs`.
7. Example read-only call: `curl -H 'X-Allowed-Project: ALPHA' http://127.0.0.1:8001/projects/ALPHA/sprints/12/issues`.
8. For W3, run `docker compose up -d db` and use pgvector. Your implementation should add the ingestion pipeline.

### W0 kickoff
Commands and results: [evidence/w0/w0_kickoff.md](evidence/w0/w0_kickoff.md).

### W1 prompt engineering
- Prompts: [prompts/w1/v1.md](prompts/w1/v1.md), [v2](prompts/w1/v2.md), [v3](prompts/w1/v3.md)
- Predictions: [w1_predictions.csv](evidence/w1/w1_predictions.csv), [v2](evidence/w1/w1_predictions_v2.csv), [v3](evidence/w1/w1_predictions_v3.csv)
- Comparison: [evidence/w1/w1_v1_v2_v3_compare.md](evidence/w1/w1_v1_v2_v3_compare.md)
- Error reasons: [evidence/w1/w1_error_reasons.md](evidence/w1/w1_error_reasons.md)
- Score: `python scripts/evaluate_issue_classifier.py evidence/w1/w1_predictions_v3.csv`

### W2 LLM API & structured output (GATE 1)
Provider: OpenAI. W1 model: `OPENAI_MODEL` (ví dụ `gpt-4.1`). W2 model: `W2_MODEL` (ví dụ `gpt-6-luna`). Cần `OPENAI_API_KEY` và `OPENAI_BASE_URL=https://api.openai.com/v1`.

Chạy API + demo (từ thư mục gốc repo):
```bash
env $(grep -E "^(OPENAI_API_KEY|OPENAI_BASE_URL|W2_MODEL)=" .env | xargs) .venv/bin/uvicorn app.main:app --port 8000
```
- OpenAPI: `http://127.0.0.1:8000/docs`
- Demo UI: `http://127.0.0.1:8000/demo`

Gọi thử:
```bash
curl -s -X POST http://127.0.0.1:8000/analyze-meeting \
  -H 'Content-Type: application/json' \
  -d '{"meeting_text":"Meeting Date: 2026-11-23\nAttendees: Phu, Hung\n\nThe team agreed to prioritize the login bug. Phu will fix authentication by November 25, 2026."}'
```

| Tình huống | HTTP |
|---|---|
| Input rỗng / dưới 20 ký tự | 422 |
| Timeout upstream | 504 |
| Rate limit (429) | 429 |
| Upstream 5xx / lỗi kết nối | 502 |
| JSON sai khuôn sau retry | 502 |

Test và eval:
```bash
.venv/bin/python -m pytest -q tests/test_w2_errors.py tests/test_mock_jira.py
.venv/bin/python scripts/evaluate_w2_meetings.py
```
- Walkthrough: [evidence/w2/w2_walkthrough.md](evidence/w2/w2_walkthrough.md)
- Eval JSON: [evidence/w2/w2_eval.json](evidence/w2/w2_eval.json)
- Error reasons: [evidence/w2/w2_error_reasons.md](evidence/w2/w2_error_reasons.md)
- HTTP examples: [evidence/w2/analyze_meeting.http](evidence/w2/analyze_meeting.http)

### Resource map
- `data/documents/`: 15 synthetic documents plus manifest (5 requirements, 5 technical, 5 PM)
- `data/jira/issues.json`: 30 sample issue records for Projects ALPHA/BETA/GAMMA
- `data/evaluation/`: 20 labeled issue cases, 20 retrieval queries, 30 RAG cases, 20 agent scenarios, 10 security cases
- `app/mock_jira.py`: working read-only mock Jira API for W5 onward
- `scripts/evaluate_issue_classifier.py`: scoring harness; supply CSV with headers `issue_id,predicted_category,predicted_priority`
- `evidence/weekly_pr_template.md`: required PR/evidence structure
- `assignments/`: weekly handoff instructions; slide deck contains full requirements and PASS criteria

## Safety and limitations
- **TRAINING FIXTURES ONLY.** Do not copy real customer data into model APIs without written approval.
- Mock authorization via `X-Allowed-Project` is **not suitable for production**. Replace with identity, authentication and server-side authorization in W7.
- LLM responses are nondeterministic; test using consistent model configuration, recorded prompt versions and human-reviewed evaluations.
- Hidden mentor assessment fixtures must remain **separate from this member-facing kit**.
- The `requirements.txt` pins broad compatible release families; AI Lead should lock tested versions before program rollout.
- No company-specific Git URL, API credentials, staging URLs or mentor contacts are invented. AI Lead must fill those in during kickoff.
