# Kết quả V1 (W1)

- Prompt: `prompts/w1/v1.md`
- Model: `gpt-4.1`, `temperature=0`
- Kết quả: `evidence/w1/w1_predictions.csv`

| Tiêu chí | Kết quả | Mức đạt | Trạng thái |
|---|---|---|---|
| Category | 20/20 | ≥ 17/20 | Đạt |
| Schema | 20/20 | 20/20 | Đạt |
| P1 bỏ sót | CASE-16 | 0 | Không đạt |
| Priority | 16/20 | không có mức đạt | Tham khảo |

## Case lệch priority

| Case | Gold | V1 |
|---|---|---|
| CASE-07 | Feature / P2 | Feature / P3 |
| CASE-12 | Question / P2 | Question / P3 |
| CASE-13 | Risk / P2 | Risk / P1 |
| CASE-16 | Risk / P1 | Risk / P2 |

CSV không lưu lý do của model.
