# W2 PR description

Copy vào GitHub PR theo `evidence/weekly_pr_template.md`.

**Member:** _(điền tên)_

**Feature (F01 foundation / Gate 1):**  
`POST /analyze-meeting` — trích xuất `summary`, `decisions`, `actions` từ biên bản họp bằng OpenAI Structured Outputs (strict) + validate Pydantic; xử lý lỗi HTTP; demo UI so sánh gold; eval ≥17/20.

**What I studied:**
- Docs: [OpenAI Developer Quickstart](https://developers.openai.com/api/docs/quickstart), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Function Calling](https://developers.openai.com/api/docs/guides/function-calling), [Streaming](https://developers.openai.com/api/docs/guides/streaming-responses)
- Ghi chú: `learning/OpenAI_Quickstart_Tong_ket.md`, `learning/OpenAI_Structured_Outputs_Tong_ket.md`, `learning/w2_openai_structured_outputs.md`
- Lab: `learning/labs/main.py`, `structure_output.py`, `function-calling.py`, `streaming.py`
- Áp dụng W2: Pydantic input/output; timeout / 429 / upstream / bad JSON retry; LLM-as-judge summary trên demo (không tính Gate)

**What I built (summary + key modules):**
- `app/schemas.py` — `MeetingRequest` (≥20 ký tự), `Summary`, `ActionItem`
- `app/services/llm.py` — `analyze()` + `judge_summary()` (openai SDK, json_schema strict)
- `app/scoring.py` — `check()` (số decisions/actions + owner + due_date)
- `app/main.py` — `/analyze-meeting`, `/demo`, `/demo-api/cases`, `/demo-api/compare`, `/demo-api/judge-summary`
- `app/static/demo.html` — Run / Run all + popup Xem KQ / Chấm summary
- `tests/test_w2_errors.py` — 6 test mock (422, 504, 429, 502×2, schema)
- `scripts/evaluate_w2_meetings.py` — eval 20 case (`check` only; summary judge deferred)
- Evidence: `w2_eval.json`, `w2_walkthrough.md`, `w2_slides.md`, `analyze_meeting.http`

**How to run:**
```bash
env $(grep -E "^(OPENAI_API_KEY|OPENAI_BASE_URL|W2_MODEL)=" .env | xargs) .venv/bin/uvicorn app.main:app --port 8000
.venv/bin/python -m pytest -q tests/test_w2_errors.py tests/test_mock_jira.py
.venv/bin/python scripts/evaluate_w2_meetings.py
```
- Docs: `http://127.0.0.1:8000/docs`
- Demo: `http://127.0.0.1:8000/demo`

**Results:**
- Schema: **20/20**
- Extraction (`check`): **20/20** (Gate ≥17 → PASS)
- Error tests: **6 passed**; mock Jira: **3 passed**; smoke: PASS
- Summary judge: có trên demo (`/demo-api/judge-summary`); eval batch `deferred` (không tính Gate)

**Known limitations / trade-offs:**
- Không còn case FAIL theo `check()` lần eval hiện tại (`w2_eval.json`)
- Bộ case = mentor public set; mục E (tự viết 20 case) chưa làm
- Gate không chấm semantic chữ decision/action/summary; summary judge tách riêng

**Demo link:** `http://127.0.0.1:8000/demo` (+ `/docs`)  
**Slides present:** `evidence/w2/w2_slides.md`

**PR link:** _(điền sau khi mở PR)_

**Next action:**
1. **Chốt W2 nộp:** video màn hình · mở PR `w2` · gửi mentor (slides: `w2_slides.md`).
2. **Chuẩn bị W3** (30/11–04/12 — Embeddings & semantic search · F01 search):
   - Học: DeepLearning.AI Vector Databases; [OpenAI Retrieval](https://platform.openai.com/docs/guides/retrieval)
   - Máy: Docker + `docker compose up -d db` (pgvector); kiểm tra `DATABASE_URL` trong `.env`
   - Đọc sẵn: `data/documents/` (15 file + `manifest.json`), `data/evaluation/retrieval_gold.json` (20 query)
   - Làm: bảng chunk (text, embedding, doc_id, project_id, source/offset) · `ingest.py` · `POST/GET /search` top-5 · **filter `project_id` trong SQL**
   - Pass: 15/15 index · Recall@5 ≥ 80% · 0 rò rỉ cross-project · giải thích chunk size / top-k / similarity
