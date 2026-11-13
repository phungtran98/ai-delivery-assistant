# Weekly Submission – W1 / Member __

**Feature (F01–F04 or Foundation):** Foundation. Phân loại issue Jira giả: category và priority.

**What I studied (2–3 concepts):**

- Prompt gồm luật, input trong `"""`, và schema JSON.
- Structured output: model trả JSON, Pydantic kiểm tra `category`, `priority`, `next_actions`.
- Đo chất lượng bằng script có sẵn, so CSV với gold. Script không gọi model.

**What I built (summary + key modules):**

- `prompts/w1/v1.md`, `v2.md`, `v3.md`
- `scripts/classify_one.py`: một case. `scripts/run_v1.py`: 20 case, ghi CSV.
- Model `gpt-4.1`, `temperature=0`.
- CSV: `evidence/w1/w1_predictions.csv`, `w1_predictions_v2.csv`, `w1_predictions_v3.csv`
- So sánh: `evidence/w1/w1_v1_v2_v3_compare.md`
- Lý do các case sai: `evidence/w1/w1_error_reasons.md` (người viết đối chiếu, model không ghi lý do)

**How to run:**

```bash
.venv/bin/python scripts/classify_one.py CASE-16 prompts/w1/v3.md
.venv/bin/python scripts/run_v1.py prompts/w1/v3.md evidence/w1/w1_predictions_v3.csv
.venv/bin/python scripts/evaluate_issue_classifier.py evidence/w1/w1_predictions_v3.csv
```

**Results:**

| Chỉ số | V1 | V2 | V3 | Mức đạt |
|---|---|---|---|---|
| Category | 20/20 | 20/20 | 20/20 | ≥ 17/20 |
| Schema | 20/20 | 20/20 | 20/20 | 20/20 |
| Priority | 16/20 | 15/20 | 18/20 | không có mức đạt |
| P1 bỏ sót | CASE-16 | không | không | không được bỏ sót |

V3 đạt category, schema và không bỏ sót P1. V1 không đạt vì bỏ sót CASE-16.

**Known failures / trade-offs:**

- V3 được sửa sau khi xem lỗi V2 trên đúng 20 case này. Điểm V3 không phải đánh giá trên case mới.
- Cùng prompt V3, `temperature=0`: một lần 19/20 (chỉ sai CASE-07), lần đang nộp 18/20 (sai CASE-17 và CASE-18).
- CSV không lưu lý do của model.
- Bộ 20 case là fixture public. Mentor giữ 20–30% case ẩn ngoài kit. Lần này chưa chấm tập đó.

**Demo link:** `evidence/w1/w1_demo.html` (chưa có link công khai)

**PR link:**
