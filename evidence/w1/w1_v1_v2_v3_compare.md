# So sánh V1, V2, V3 (W1)

Model `gpt-4.1`, `temperature=0`. V2 chỉ đổi định nghĩa P1 so với V1. V3 chỉnh định nghĩa P1, P2, P3 so với V2.

| Chỉ số | V1 | V2 | V3 |
|---|---|---|---|
| Category | 20/20 | 20/20 | 20/20 |
| Schema | 20/20 | 20/20 | 20/20 |
| Priority | 16/20 | 15/20 | 18/20 |
| P1 bỏ sót | CASE-16 | không | không |

## Case khác nhau giữa các phiên bản

| Case | Gold | V1 | V2 | V3 |
|---|---|---|---|---|
| CASE-07 | Feature / P2 | Feature / P3 | Feature / P3 | Feature / P2 |
| CASE-08 | Feature / P3 | Feature / P3 | Feature / P2 | Feature / P3 |
| CASE-12 | Question / P2 | Question / P3 | Question / P3 | Question / P2 |
| CASE-13 | Risk / P2 | Risk / P1 | Risk / P1 | Risk / P2 |
| CASE-16 | Risk / P1 | Risk / P2 | Risk / P1 | Risk / P1 |
| CASE-17 | Bug / P2 | Bug / P2 | Bug / P2 | Bug / P1 |
| CASE-18 | Feature / P2 | Feature / P2 | Feature / P2 | Feature / P3 |
| CASE-20 | Risk / P2 | Risk / P2 | Risk / P1 | Risk / P2 |

V2 sửa được CASE-16 và hết P1 bỏ sót, nhưng kéo CASE-08 và CASE-20 lên P2/P1. V3 sửa được CASE-07, CASE-08, CASE-12, CASE-13 và CASE-20, giữ CASE-16 ở P1. V3 sai CASE-17 và CASE-18.

V3 được chỉnh sau khi xem lỗi của V2 trên cùng 20 case, nên điểm V3 không phải đánh giá khách quan. Cùng prompt V3 đã cho 19/20 ở lần chạy đầu và 18/20 ở lần chạy sau, nên priority không ổn định hoàn toàn ở `temperature=0`.

## V3 so với V1

- Cả V1 và V3 đều đạt category 20/20 và schema 20/20.
- V1 bỏ sót P1 là CASE-16. V3 không bỏ sót P1 nào.
- Priority: V3 18/20, V1 16/20.
- V3 đúng hơn V1 ở CASE-07, CASE-12, CASE-13 và CASE-16. V1 sai cả bốn case này.
- V3 sai hơn V1 ở CASE-17 và CASE-18. V1 đúng cả hai case này.
- Định nghĩa P1 trong V3 nêu rõ "đã biết không có phương án dự phòng", nên CASE-16 được gán P1 đúng.
- Định nghĩa P2 trong V3 nêu rõ "field trong báo cáo", "ai sẽ duyệt báo cáo sự cố" và "có thể / chưa review làm trễ mốc", nên CASE-07, CASE-12 và CASE-13 được gán đúng mức.
