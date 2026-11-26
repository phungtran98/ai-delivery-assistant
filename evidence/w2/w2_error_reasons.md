# W2 – Lý do case sai (lần eval 18/20)

Nguồn: `evidence/w2/w2_eval.json` sau khi chạy `scripts/evaluate_w2_meetings.py` với prompt hiện tại. Lý do do người viết đối chiếu `expected` và `predicted`, không phải do model tự giải thích.

## TC07 – Documentation Update (Missing information)

- **Gold:** 1 decision `Improve the API documentation.`; 1 action `owner=null`, `due_date=2026-11-30`.
- **Model:** 0 decision; 1 action `owner=null`, `due_date=2026-11-30`.
- **Khớp:** owner null và ngày đúng (không đoán từ attendees).
- **Sai:** thiếu decision. Biên bản có thỏa thuận cải thiện tài liệu API; model chỉ lấy action cập nhật endpoint description.
- **Quy tắc liên quan:** `evaluation_notes` ghi unknown owner phải null; không nói rõ “agreement without owner vẫn là decision”.

## TC09 – Code Quality Discussion (Missing information)

- **Gold:** 1 decision `Refactoring is necessary...`; 0 action.
- **Model:** 0 decision; 0 action.
- **Khớp:** không bịa action (đúng notes: agreement là decision, không invent assignment).
- **Sai:** thiếu decision. Biên bản ghi team agreed refactoring is necessary nhưng không giao việc; model để trống cả decisions.
- **Quy tắc liên quan:** prompt có “decision is only something the team agreed to do”, nhưng model vẫn bỏ qua agreement không kèm action.
