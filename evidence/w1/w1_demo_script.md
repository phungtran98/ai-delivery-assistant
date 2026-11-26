# Kịch bản demo W1 (5 phút)

Mở sẵn trước khi nói:

- Terminal ở thư mục gốc repo.
- File `evidence/w1/w1_v1_v2_v3_compare.md`.
- File `evidence/w1/w1_predictions.csv` và `evidence/w1/w1_predictions_v3.csv`.

Nếu lệnh live ra khác file CSV, nói: "Lần chạy lúc này khác file đã chấm. Em lấy số trong CSV đã nộp." Rồi chỉ vào dòng CASE-16 trong hai file CSV.

## 0:00 — Bài toán

Em phân loại 20 issue Jira giả. Mỗi issue có một category: Bug, Feature, Question, hoặc Risk. Và một priority: P1, P2, hoặc P3.

Đề yêu cầu category đúng ít nhất 17 trên 20, JSON đúng khuôn 20 trên 20, và không bỏ sót P1. Sáu case P1 là CASE-01, 02, 03, 04, 14 và 16.

## 0:30 — Cách đo

Em viết ba prompt: V1, V2, V3. Mỗi prompt chạy 20 request riêng. Model là gpt-4.1, temperature bằng 0. Script parse JSON bằng Pydantic. Nếu sai khuôn thì thử lại một lần, vẫn sai thì ghi INVALID.

Bộ chấm là script có sẵn của kit: `scripts/evaluate_issue_classifier.py`. Script này không gọi model. Nó so CSV với file gold.

## 1:00 — Chạy một case

Case demo là CASE-16: "No fallback if external OAuth is down". Gold là Risk, P1.

Chạy V1:

```bash
.venv/bin/python scripts/classify_one.py CASE-16
```

Chỉ vào dòng `parsed` và dòng `gold`. Trong CSV đã chấm, V1 ra Risk P2. Gold là Risk P1. Đây là P1 bị bỏ sót.

Chạy V3, cùng case, đổi file prompt:

```bash
.venv/bin/python scripts/classify_one.py CASE-16 prompts/w1/v3.md
```

Trong CSV đã chấm, V3 ra Risk P1, khớp gold. Khác nhau nằm ở định nghĩa P1: V3 ghi rõ trường hợp đã biết là không có phương án dự phòng.

## 2:30 — Bảng điểm

Mở `evidence/w1/w1_v1_v2_v3_compare.md`.

| Chỉ số | V1 | V2 | V3 |
|---|---|---|---|
| Category | 20/20 | 20/20 | 20/20 |
| Schema | 20/20 | 20/20 | 20/20 |
| Priority | 16/20 | 15/20 | 18/20 |
| P1 bỏ sót | CASE-16 | không | không |

Cả ba bản đều qua category và schema. V1 không qua vì bỏ sót CASE-16. V2 và V3 không bỏ sót P1. Priority không có ngưỡng đạt trong đề.

## 3:30 — Vì sao V3 tốt hơn V1

V3 đúng thêm bốn case mà V1 sai: CASE-07, CASE-12, CASE-13 và CASE-16.

V3 cũng sai hai case mà V1 đúng: CASE-17 và CASE-18. Priority V3 là 18/20, V1 là 16/20.

V2 chỉ sửa định nghĩa P1 nên hết bỏ sót P1, nhưng priority giảm xuống 15/20. V3 sửa tiếp P2 và P3.

## 4:30 — Hạn chế

V3 được sửa sau khi em đã xem lỗi của V2 trên đúng 20 case này. Điểm V3 không phải đánh giá trên bộ case mới.

Cùng prompt V3, lần chạy đầu ra 19/20, lần sau ra 18/20. Temperature bằng 0 chưa làm kết quả giống hệt nhau.

CSV không lưu lý do của model, nên em không giải thích được vì sao model chọn từng nhãn.

Việc tiếp theo: ghi lý do các case còn sai, mở PR theo `evidence/weekly_pr_template.md`, gửi link cho mentor.
