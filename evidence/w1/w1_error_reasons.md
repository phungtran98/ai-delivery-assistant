# Lý do các case sai (W1)

Lý do dưới đây do người viết đối chiếu nội dung issue, nhãn gold và điều kiện trong prompt. CSV và model không ghi lý do.

- Prompt: `prompts/w1/v1.md`, `v2.md`, `v3.md`
- CSV: `evidence/w1/w1_predictions.csv` (V1), `w1_predictions_v2.csv` (V2), `w1_predictions_v3.csv` (V3)
- Lỗi category: không có. Cả ba bản đều 20/20 category. Các lỗi dưới đây đều là lỗi priority.

## Tổng hợp

| Case | Gold | V1 | V2 | V3 |
|---|---|---|---|---|
| CASE-07 | P2 | P3 sai | P3 sai | đúng |
| CASE-08 | P3 | đúng | P2 sai | đúng |
| CASE-12 | P2 | P3 sai | P3 sai | đúng |
| CASE-13 | P2 | P1 sai | P1 sai | đúng |
| CASE-16 | P1 | P2 sai | đúng | đúng |
| CASE-17 | P2 | đúng | đúng | P1 sai |
| CASE-18 | P2 | đúng | đúng | P3 sai |
| CASE-20 | P2 | đúng | P1 sai | đúng |

Số case sai: V1 4 case, V2 5 case, V3 2 case.

## V1 — 4 case sai

### CASE-07
- Gold: Feature P2. V1: Feature P3.
- Issue: "Add a custom Jira field in status report"
- Điều kiện khớp: P3 "việc thường, không gấp".
- Điều kiện thiếu: V1 không có điều kiện nào về field trong báo cáo. P2 chỉ có "phạm vi hẹp hơn" và không có mốc so sánh, nên không tách được khỏi P3.

### CASE-12
- Gold: Question P2. V1: Question P3.
- Issue: "Who must approve an incident report?"
- Điều kiện khớp: P3 "chỉ hỏi thông tin".
- Điều kiện thiếu: V1 không có điều kiện nào về việc duyệt báo cáo sự cố. V3 có điều kiện này trong P2: "câu hỏi về ai sẽ duyệt báo cáo sự cố".

### CASE-13
- Gold: Risk P2. V1: Risk P1.
- Issue: "Vendor API may miss December cutover"
- Điều kiện khớp: P1 "chặn go-live". Issue nhắc đến cutover tháng 12.
- Điều kiện thiếu: V1 P1 không phân biệt rủi ro "có thể" với việc đã chắc chắn. Issue dùng "may". V3 P2 có điều kiện "rủi ro chỉ ở mức 'có thể' ... làm trễ mốc thời gian".

### CASE-16
- Gold: Risk P1. V1: Risk P2.
- Issue: "No fallback if external OAuth is down"
- Điều kiện khớp: P2 "rủi ro cần xử lý trước deadline", vì issue là một rủi ro.
- Điều kiện thiếu: P1 của V1 không khớp, vì issue không nói nhiều user hay chặn go-live. V1 không có điều kiện về phương án dự phòng. V2 và V3 đều thêm điều kiện này vào P1.

## V2 — 5 case sai

V2 chỉ đổi P1 so với V1. P2 và P3 giữ nguyên, nên CASE-07 và CASE-12 vẫn sai như V1.

### CASE-07
- Gold: Feature P2. V2: Feature P3.
- Issue: "Add a custom Jira field in status report"
- Điều kiện khớp: P3 "việc thường, không gấp".
- Điều kiện thiếu: V2 không có điều kiện về field trong báo cáo. Điều kiện P2 "phạm vi hẹp hơn" không có mốc so sánh.

### CASE-08
- Gold: Feature P3. V2: Feature P2.
- Issue: "Support export of reports as CSV"
- Điều kiện khớp: P2 "phạm vi hẹp hơn". Issue chỉ là một tính năng xuất CSV.
- Điều kiện thiếu: V2 không có điều kiện nào đưa định dạng xuất file về P3. V3 thêm "định dạng xuất file" vào P3.

### CASE-12
- Gold: Question P2. V2: Question P3.
- Issue: "Who must approve an incident report?"
- Điều kiện khớp: P3 "chỉ hỏi thông tin".
- Điều kiện thiếu: V2 không có điều kiện về việc duyệt báo cáo sự cố. Điều kiện này có trong V3 P2.

### CASE-13
- Gold: Risk P2. V2: Risk P1.
- Issue: "Vendor API may miss December cutover"
- Điều kiện khớp: P1 "rủi ro chặn go-live". V2 thêm chữ "rủi ro" vào điều kiện này, nên issue khớp P1.
- Điều kiện thiếu: V2 P1 không phân biệt rủi ro "có thể" với rủi ro đã chắc chắn.

### CASE-20
- Gold: Risk P2. V2: Risk P1.
- Issue: "Unreviewed dependencies could delay release"
- Điều kiện khớp: P1 "rủi ro không có phương án dự phòng cho một phụ thuộc quan trọng". Issue có chữ "dependencies".
- Điều kiện thiếu: issue không nói gì về phương án dự phòng. Issue nói "unreviewed", và điều kiện "chưa review làm trễ mốc" nằm trong V3 P2, không có trong V2.

## V3 — 2 case sai

### CASE-17
- Gold: Bug P2. V3: Bug P1 trong lần chạy 18/20. Lần chạy khác của cùng prompt ra P2 khi gọi `classify_one.py` (log terminal ngày 13/11).
- Issue: "Sort order changes unexpectedly on issues page"
- Điều kiện khớp: P1 "đang hỏng". Issue là một Bug.
- Điều kiện thiếu: P1 yêu cầu "ảnh hưởng đến nhiều người dùng ngay lúc này". Issue không nói có nhiều người dùng. V3 P2 không có điều kiện nào cho lỗi phạm vi hẹp, nên không có chỗ để xếp lỗi này.

### CASE-18
- Gold: Feature P2. V3: Feature P3.
- Issue: "Change report frequency from weekly to daily"
- Điều kiện khớp: P3 "thêm chức năng mới" theo category Feature.
- Điều kiện thiếu: V3 P2 chỉ nêu "thay đổi ngày tháng trong báo cáo hoặc quy trình duyệt". Issue nói tần suất, không nói ngày tháng. Không có điều kiện nào trong V3 nêu rõ việc đổi tần suất báo cáo.
- Ghi chú: gold JSON chỉ có nhãn, không có lý do. Vì vậy lý do gold P2 cho case này không có căn cứ trong kit.
