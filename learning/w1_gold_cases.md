# Gold set: phân loại issue (W1)

Nguồn: `data/evaluation/issue_classification_gold.json` (đọc-only, không sửa). Có 20 case.

## Các field

- `issue_id`: mã case, dạng CASE-01 đến CASE-20.
- `text`: nội dung issue, được thay vào `{issue_text}` trong prompt.
- `text_vi`: bản dịch tiếng Việt của `text`. Chỉ để đọc, không đưa vào prompt và không nằm trong file gold.
- `category`: một trong Bug, Feature, Question, Risk. Đây là gold label.
- `priority`: một trong P1, P2, P3. Đây là gold label.

## Danh sách case

| issue_id | text | text_vi | category (gold) | priority (gold) |
|---|---|---|---|---|
| CASE-01 | Production checkout API down for all users | API checkout production đang ngừng với tất cả người dùng | Bug | P1 |
| CASE-02 | Critical payment processing fails globally | Xử lý thanh toán quan trọng đang thất bại trên toàn hệ thống | Bug | P1 |
| CASE-03 | Data export returns 500 for all customers | Xuất dữ liệu trả về lỗi 500 với tất cả khách hàng | Bug | P1 |
| CASE-04 | Passwords accepted but SSO blocks all logins | Mật khẩu được chấp nhận nhưng SSO chặn mọi lần đăng nhập | Bug | P1 |
| CASE-05 | Add download button to sprint chart | Thêm nút tải xuống vào biểu đồ sprint | Feature | P3 |
| CASE-06 | Implement dark theme on PM dashboard | Triển khai giao diện tối trên dashboard PM | Feature | P3 |
| CASE-07 | Add a custom Jira field in status report | Thêm một field Jira tùy chỉnh trong báo cáo trạng thái | Feature | P2 |
| CASE-08 | Support export of reports as CSV | Hỗ trợ xuất báo cáo dưới dạng CSV | Feature | P3 |
| CASE-09 | What is the expected UAT deadline? | Thời hạn UAT dự kiến là khi nào? | Question | P3 |
| CASE-10 | How many issues are in the current sprint? | Sprint hiện tại có bao nhiêu issue? | Question | P3 |
| CASE-11 | Where are weekly release notes stored? | Release notes hàng tuần được lưu ở đâu? | Question | P3 |
| CASE-12 | Who must approve an incident report? | Ai phải duyệt báo cáo sự cố? | Question | P2 |
| CASE-13 | Vendor API may miss December cutover | API của nhà cung cấp có thể bỏ lỡ đợt cutover tháng 12 | Risk | P2 |
| CASE-14 | Security certificate expires before go-live | Chứng chỉ bảo mật hết hạn trước khi go-live | Risk | P1 |
| CASE-15 | Single reviewer may delay UAT sign-off | Một người review duy nhất có thể làm chậm việc ký UAT | Risk | P2 |
| CASE-16 | No fallback if external OAuth is down | Không có phương án dự phòng nếu OAuth bên ngoài bị lỗi | Risk | P1 |
| CASE-17 | Sort order changes unexpectedly on issues page | Thứ tự sắp xếp thay đổi bất ngờ ở trang issues | Bug | P2 |
| CASE-18 | Change report frequency from weekly to daily | Đổi tần suất báo cáo từ hàng tuần sang hàng ngày | Feature | P2 |
| CASE-19 | Which region hosts our staging cluster? | Staging cluster của chúng ta nằm ở region nào? | Question | P3 |
| CASE-20 | Unreviewed dependencies could delay release | Các phụ thuộc chưa được review có thể làm trễ release | Risk | P2 |

## Thống kê

- Category: Bug 5, Feature 5, Question 5, Risk 5.
- Priority: P1 6, P2 7, P3 7.
- Case P1: CASE-01, CASE-02, CASE-03, CASE-04, CASE-14, CASE-16.
