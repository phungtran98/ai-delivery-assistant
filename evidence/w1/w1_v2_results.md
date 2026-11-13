# Kết quả V2 (W1)

- Prompt: `prompts/w1/v2.md` (chỉ đổi định nghĩa P1 so với V1)
- Model: `gpt-4.1`, `temperature=0`
- Kết quả: `evidence/w1/w1_predictions_v2.csv`

| Tiêu chí | Kết quả | Mức đạt | Trạng thái |
|---|---|---|---|
| Category | 20/20 | ≥ 17/20 | Đạt |
| Schema | 20/20 | 20/20 | Đạt |
| P1 bỏ sót | không | 0 | Đạt |
| Priority | 15/20 | không có mức đạt | Tham khảo |

## Case lệch priority

| Case | Gold | V2 |
|---|---|---|
| CASE-07 | Feature / P2 | Feature / P3 |
| CASE-08 | Feature / P3 | Feature / P2 |
| CASE-12 | Question / P2 | Question / P3 |
| CASE-13 | Risk / P2 | Risk / P1 |
| CASE-20 | Risk / P2 | Risk / P1 |

CSV không lưu lý do của model.
