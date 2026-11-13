# Kết quả V3 (W1)

- Prompt: `prompts/w1/v3.md` (chỉnh P1, P2, P3 so với V2 sau khi xem lỗi V2)
- Model: `gpt-4.1`, `temperature=0`
- Kết quả: `evidence/w1/w1_predictions_v3.csv`

| Tiêu chí | Kết quả | Mức đạt | Trạng thái |
|---|---|---|---|
| Category | 20/20 | ≥ 17/20 | Đạt |
| Schema | 20/20 | 20/20 | Đạt |
| P1 bỏ sót | không | 0 | Đạt |
| Priority | 18/20 | không có mức đạt | Tham khảo |

## Case lệch priority

| Case | Gold | V3 |
|---|---|---|
| CASE-17 | Bug / P2 | Bug / P1 |
| CASE-18 | Feature / P2 | Feature / P3 |

CSV không lưu lý do của model.

Cùng prompt V3 đã chạy hai lần ở `temperature=0`: lần đầu 19/20 (lệch CASE-07), lần sau 18/20 (lệch CASE-17 và CASE-18). Kết quả priority thay đổi giữa hai lần chạy.
