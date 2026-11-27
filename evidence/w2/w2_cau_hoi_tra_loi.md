# W2 · Câu hỏi & câu trả lời (chuẩn bị họp sếp / mentor)

Nguồn: `w2_slides.md`, `w2_walkthrough.md`, `app/services/llm.py`, `app/scoring.py`, `app/schemas.py`.  
Kết quả Gate hiện tại: schema **20/20**, extraction **20/20**, error tests **6 passed**.

---

## Pitch 30 giây

> Tuần 2 mình đóng gói LLM thành REST API `POST /analyze-meeting`: trích xuất summary, decisions, actions bằng OpenAI Structured Outputs (strict) + validate Pydantic. Map lỗi rõ ràng (422 / 504 / 429 / 502), không crash. Gate chấm số decisions/actions và cặp `(owner, due_date)`; đạt 20/20. Summary judge tách riêng trên demo, không tính điểm nộp.

---

## A. Overview

### 1. Tuần 2 làm gì? Mục tiêu Gate 1 là gì?

**Trả lời:** Đóng gói LLM thành REST API đáng tin cậy. Endpoint chính là `POST /analyze-meeting`: nhận biên bản họp, trả `summary`, `decisions`, `actions` (owner, due_date). Gate 1 yêu cầu: chạy được + `/docs`, 100% đúng schema, ≥17/20 trích xuất đúng, 5/5 kịch bản lỗi pass, không lộ API key.

### 2. Vì sao đóng gói LLM thành REST API thay vì gọi model trong script?

**Trả lời:** API có contract rõ (schema request/response), validate input, map lỗi HTTP chuẩn, dễ demo/test/tích hợp client. Script một lần không có timeout/retry/status code thống nhất cho phía gọi.

### 3. Kết quả Gate của bạn?

**Trả lời:** Schema 20/20, extraction (`check`) 20/20, error tests 6 passed, mock Jira 3 passed, smoke PASS. Evidence: `evidence/w2/w2_eval.json`.

### 4. Demo chạy thế nào?

**Trả lời:** `uvicorn app.main:app --port 8000` → `/docs` thử API, `/demo` chọn case → Run so sánh Gold | AI, Run all bảng điểm, nút Chấm summary (tuỳ chọn).

---

## B. Kiến trúc & luồng

### 5. Request đi từ client đến model rồi về thế nào?

**Trả lời:**

```text
Client POST /analyze-meeting
  → Pydantic MeetingRequest (≥20 ký tự)
  → llm.analyze() → OpenAI chat.completions + json_schema strict
  → Summary.model_validate_json
  → 200 Summary
  lỗi → 422 / 504 / 429 / 502
```

### 6. Vì sao tách `llm.py` khỏi `main.py`?

**Trả lời:** `main.py` chỉ lo HTTP (route, status). `llm.py` lo gọi model, prompt, schema, retry JSON. Tách giúp mock LLM khi test lỗi, đổi model/provider không đụng route.

### 7. Schema response gồm field nào? Khi nào `null`?

**Trả lời:**

```json
{
  "summary": "string",
  "decisions": ["string"],
  "actions": [
    { "owner": "string|null", "action": "string", "due_date": "YYYY-MM-DD|null" }
  ]
}
```

Owner/ngày không rõ → `null`. Ngày tương đối (vd. “next Friday”) → `due_date = null`. Không đoán.

### 8. Input dưới 20 ký tự xử lý ra sao?

**Trả lời:** `MeetingRequest.meeting_text` dùng `min_length=20` → FastAPI/Pydantic trả **422**, không gọi OpenAI.

---

## C. Structured Outputs

### 9. Structured Outputs khác “nhờ model trả JSON” / JSON mode thế nào?

**Trả lời:** Structured Outputs ép đúng JSON Schema đã khai báo (`response_format: json_schema`, `strict: true`). JSON mode chỉ ép cú pháp JSON, không đảm bảo đúng field/type. W2 dùng schema từ Pydantic `Summary.model_json_schema()` rồi chỉnh cho strict.

### 10. `strict: true` bắt buộc điều gì?

**Trả lời:** Mỗi object: `additionalProperties: false` và `required` liệt kê đủ mọi key trong `properties`. Code có hàm `strict_schema()` làm việc này trước khi gửi API.

### 11. Vì sao vẫn validate Pydantic sau khi model đã trả schema?

**Trả lời:** Phòng khi content rỗng/lệch, hoặc provider không tuân thủ 100%. `Summary.model_validate_json(...)` fail → coi là bad JSON → retry hoặc 502.

### 12. Model trả JSON hỏng thì sao?

**Trả lời:** Retry tối đa 2 lần trong `analyze()`. Hỏng cả 2 → `LLMError("bad_output")` → HTTP **502**. SDK `max_retries=0` để tự kiểm soát retry, không để SDK retry ngầm.

---

## D. Prompt & quy tắc trích xuất

### 13. Thế nào là decision? Proposal / postponed / “no decision” có tính không?

**Trả lời:** Decision = team **đã đồng ý** rõ (kể cả “needs improvement”, “is necessary”). Không tạo decision từ “no decision was made”, postponed, hay proposal/suggestion suông.

### 14. “Next Friday” và ngày thiếu năm?

**Trả lời:** Ngày tương đối → `due_date = null`. Ngày tuyệt đối thiếu năm → lấy năm từ ngày họp. Absolute date → `YYYY-MM-DD`.

### 15. Task giao 2 người → mấy action?

**Trả lời:** Một action cho mỗi người (không gộp một action nhiều owner).

### 16. Team dời deadline → mấy decision?

**Trả lời:** Một decision ghi hạn mới. Không tách thêm decision “hạn cũ hết hiệu lực”. Milestone tổng giữ tách với due_date từng người.

---

## E. Chấm điểm / Gate

### 17. `check()` so gì với gold?

**Trả lời:** (`app/scoring.py`)

- Decisions: **số lượng**
- Actions: **số lượng** + từng cặp `(owner, due_date)` có trong predicted
- **Không** so chữ summary / decision / action text

### 18. Vì sao Gate chỉ đếm số + owner/date?

**Trả lời:** Metric rule-based, dễ giải thích, ổn định, không phụ thuộc model chấm điểm. Trade-off: chưa đánh giá semantic full text của decision/action.

### 19. LLM-as-judge summary là gì? Vì sao không tính Gate?

**Trả lời:** `judge_summary()` gửi Gold + AI summary cho model, trả `{ "same_meaning": true|false }` qua structured output. Chỉ trên demo `/demo-api/judge-summary`. Không cộng vào ≥17/20 để tránh AI tự chấm điểm nộp.

### 20. Ngưỡng pass Gate?

**Trả lời:** `passed >= 17` trên 20 case **và** `schema_ok == 20`. Hiện tại 20/20.

---

## F. Độ tin cậy / lỗi HTTP

### 21. Timeout / rate limit / upstream / bad JSON → status nào?

**Trả lời:** (`main.py` map `STATUS`)

| kind | HTTP |
|---|---|
| input sai (`MeetingRequest`) | **422** |
| timeout | **504** |
| rate_limit | **429** |
| upstream | **502** |
| bad_output | **502** |

### 22. Vì sao `max_retries=0` trên SDK mà vẫn retry JSON?

**Trả lời:** Tắt retry ngầm của SDK (tránh nhân đôi timeout/429). Chỉ retry có chủ đích khi parse/validate JSON fail (tối đa 2 attempt).

### 23. Test lỗi viết thế nào không tốn tiền OpenAI?

**Trả lời:** `tests/test_w2_errors.py` mock hàm `analyze` / exception → kiểm tra 422, 504, 429, 502 (upstream + bad_output), schema. **6 passed**.

---

## G. Trade-off & next

### 24. Trade-off lớn nhất tuần này?

**Trả lời:** (1) Gate metric đơn giản — dễ giải thích nhưng chưa semantic full text. (2) Summary judge tách khỏi Gate — an toàn điểm nộp nhưng summary chất lượng chỉ quan sát trên demo. (3) Đang dùng bộ mentor public; mục E (20 case tự viết) chưa làm.

### 25. Rủi ro dùng mentor public set?

**Trả lời:** Có thể overfit prompt vào bộ đã biết. Mục E tự viết case giúp kiểm tra generalization trước khi mentor dùng bộ ẩn.

### 26. Model flaky giảm rủi ro bằng gì?

**Trả lời:** Strict schema + Pydantic validate + prompt rule rõ + retry bad JSON + map lỗi HTTP + eval 20 case cố định.

### 27. W2 nối sang W3 thế nào?

**Trả lời:** W2 = gọi LLM có contract. W3 = embeddings + semantic search trên 15 docs, filter `project_id` trong SQL, Recall@5 ≥ 80%, nền cho RAG (W4).

---

## H. Câu sâu / bẫy

### 28. Summary AI khác gold nhưng vẫn PASS — Gate có ý nghĩa không?

**Trả lời:** Có, theo **định nghĩa Gate đã chốt**: Gate đo extraction có cấu trúc (số decision/action + owner/date), không đo paraphrase summary. Summary được kiểm tra riêng bằng judge trên demo (không tính điểm). Đây là trade-off có chủ đích.

### 29. Model bịa owner từ danh sách attendee — chặn ở đâu?

**Trả lời:** Trong prompt: “If the owner is not clear, set owner = null. Do not take the owner from the attendee list.” Gate cũng fail nếu owner predicted khác gold (`null` vs tên).

### 30. API key nằm đâu? Làm sao không lộ?

**Trả lời:** `.env` (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, `W2_MODEL`). `.env` gitignore; không commit key; không log key.

### 31. Structured Outputs vs Function Calling — W2 dùng cái nào?

**Trả lời:** W2 dùng **Structured Outputs** để ép JSON kết quả extract. Function Calling / tools dùng sau (W5 agent Jira, W6 workflow). Cùng họ “schema cho model”, khác mục đích: W2 = shape của **câu trả lời**; FC = model **chọn gọi hàm** với args.

### 32. Streaming có dùng ở W2 không?

**Trả lời:** Không. W2 cần một object JSON hoàn chỉnh để validate schema. Streaming phù hợp UI chữ dần; không cần cho Gate extract.

---

## Checklist demo trước họp

1. Chạy API:  
   `env $(grep -E "^(OPENAI_API_KEY|OPENAI_BASE_URL|W2_MODEL)=" .env | xargs) .venv/bin/uvicorn app.main:app --port 8000`
2. Mở `/docs` → gọi `/analyze-meeting` (happy path).
3. Input ngắn → thấy **422**.
4. Mở `/demo` → Run 1 case → PASS/FAIL.
5. (Tuỳ chọn) Chấm summary.
6. Nhắc số liệu: **20/20 schema · 20/20 check · 6 error tests**.

---

## File liên quan

| File | Dùng để |
|---|---|
| `evidence/w2/w2_slides.md` | Slide trình bày |
| `evidence/w2/w2_walkthrough.md` | Walkthrough + workflow |
| `evidence/w2/w2_eval.json` | Bằng chứng điểm |
| `app/services/llm.py` | analyze + judge_summary |
| `app/scoring.py` | `check()` Gate |
| `app/schemas.py` | MeetingRequest / Summary / ActionItem |
