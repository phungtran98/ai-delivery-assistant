# W2 · GATE 1 — Meeting Notes API

**AI Engineering Fast-Track**  
Member: _(điền tên)_ · Nhánh `w2`

---

## 1. Mục tiêu tuần

Đóng gói LLM thành REST API đáng tin cậy:

| Mục | Nội dung |
|---|---|
| API | `POST /analyze-meeting` |
| Output | `summary` · `decisions` · `actions` (owner, due_date) |
| Kỹ thuật | Structured Outputs (strict) + Pydantic validate |
| Độ tin cậy | Timeout / 429 / upstream / bad JSON — không crash |

---

## 2. Kiến trúc

### Workflow chính — `POST /analyze-meeting`

```text
Client
  │  meeting_text
  ▼
FastAPI (main.py)
  │
  ├─ meeting_text < 20 ký tự ──────────────────────────► 422
  │
  └─ llm.analyze()  (services/llm.py)
        │
        ├─ OpenAI chat.completions
        │    response_format = json_schema strict
        │
        ├─ timeout ────────────────────────────────────► 504
        ├─ rate_limit ─────────────────────────────────► 429
        ├─ lỗi upstream ───────────────────────────────► 502
        │
        └─ content JSON
              │
              ├─ Pydantic Summary OK ──────────────────► 200
              ├─ JSON hỏng → retry ≤ 2 lần
              └─ vẫn hỏng ─────────────────────────────► 502 bad_output
```

### Workflow demo — `/demo`

```text
Chọn case → Run
  │
  ├─ 1) POST /analyze-meeting     → lấy Summary AI
  ├─ 2) POST /demo-api/compare    → scoring.check() → PASS/FAIL (Gate)
  └─ 3) [tuỳ chọn] Chấm summary
           POST /demo-api/judge-summary
             → openai judge_summary() → same_meaning true|false
             → không đổi PASS/FAIL
```

### Giải thích nhanh

| Tầng | Vai trò |
|---|---|
| `main.py` | Route HTTP, map `LLMError` → 422/504/429/502 |
| `schemas.py` | `MeetingRequest` (≥20 ký tự), `Summary`, `ActionItem` |
| `services/llm.py` | `analyze()` extract + `judge_summary()` so nghĩa |
| `scoring.py` | `check()` — số decisions/actions + cặp `(owner, due_date)` |
| `static/demo.html` | UI Run / Run all / Chấm summary |

Hai đường chấm tách biệt: **Gate** = rule Python (`check`); **summary** = model làm giám khảo (`openai` SDK + structured `{same_meaning}`), chỉ quan sát trên demo.

---

## 3. Schema response

```json
{
  "summary": "string",
  "decisions": ["string"],
  "actions": [
    { "owner": "string|null", "action": "string", "due_date": "YYYY-MM-DD|null" }
  ]
}
```

- Owner / ngày không rõ → `null` (không đoán)
- Ngày tương đối → `due_date = null`

---

## 4. Demo live

| # | Việc làm | Mục đích |
|---|---|---|
| 1 | `/docs` → gọi `/analyze-meeting` | Structured output đúng schema |
| 2 | Input quá ngắn | **422** — chặn trước khi gọi model |
| 3 | `/demo` → **Run** 1 case | So sánh Gold \| AI + PASS/FAIL |
| 4 | Nút **Chấm summary** | LLM-as-judge nghĩa summary (tuỳ chọn, không tính Gate) |
| 5 | **Run all** / bảng điểm | Tổng hợp ≥17/20 |

**Links:** `http://127.0.0.1:8000/docs` · `http://127.0.0.1:8000/demo`

---

## 5. Cách chấm Gate

| Hạng mục | Cách so với gold |
|---|---|
| Decisions | Số lượng |
| Actions | Số lượng + cặp `(owner, due_date)` |
| Summary text | **Không** tính vào Gate |
| Decision/action text | **Không** tính vào Gate |

Hàm: `app/scoring.py` → `check()` (rule-based, không gọi LLM)  
Ngưỡng: **≥ 17/20** và schema **20/20**

---

## 6. Chấm summary (LLM-as-judge) — không tính Gate

Gate dùng `check()` (rule). Summary dùng **model làm giám khảo**:

| | |
|---|---|
| Thư viện | **`openai`** (Python SDK) |
| API gọi | `client.chat.completions.create(...)` |
| Model | `W2_MODEL` (cùng model extract) |
| Ép format | **Structured Outputs** — `response_format: json_schema`, `strict: true` |
| Output | `{ "same_meaning": true \| false }` |
| Endpoint | `POST /demo-api/judge-summary` |
| Code | `llm.judge_summary()` trong `app/services/llm.py` |

**Cách hoạt động**
1. Đã có summary Gold + summary AI (sau Run)
2. Gửi hai đoạn cho model: *có cùng ý chính không?*
3. Model trả JSON boolean → UI hiện đúng nghĩa có/không

**Lưu ý:** chỉ quan sát trên demo; **không** cộng vào điểm ≥17/20.

---

## 8. Kết quả

| Tiêu chí | Kết quả |
|---|---|
| Schema | **20/20** |
| Extraction (`check`) | **20/20** |
| Error tests | **6 passed** (+ 3 mock Jira) |
| Smoke | PASS |
| Summary judge (eval batch) | deferred — có trên demo (slide 6) |

Evidence: `w2_eval.json` · `w2_walkthrough.md` · `w2_error_reasons.md`

---

## 9. Prompt / ổn định model

Đã bổ sung rule (rút gọn):

- Agreement của team (“needs improvement” / “is necessary”) → **decision**
- Không coi proposal / postponed / “no decision” là decision
- Dời hạn → **một** decision; không tách “hạn cũ hết hiệu lực”
- Milestone tổng ≠ due_date từng người

---

## 10. Trade-offs

1. Metric Gate đơn giản (count + owner/date) — dễ giải thích, chưa semantic full text  
2. Summary judge tách khỏi Gate — tránh AI tự chấm điểm nộp  
3. Đang dùng bộ case **mentor public**; bộ tự viết (mục E) chưa làm  
4. Model flaky → giảm rủi ro bằng strict schema + prompt  

---

## 11. Kết luận & next

**Gate 1:** đạt (schema · 20/20 · error handling · demo)

**Next:** PR + video màn hình · gửi mentor · (tuỳ chọn) bộ 20 case tự viết · W3 embeddings

---

## Phụ lục — lệnh chạy

```bash
env $(grep -E "^(OPENAI_API_KEY|OPENAI_BASE_URL|W2_MODEL)=" .env | xargs) \
  .venv/bin/uvicorn app.main:app --port 8000

.venv/bin/python -m pytest -q tests/test_w2_errors.py tests/test_mock_jira.py
.venv/bin/python scripts/evaluate_w2_meetings.py
```
