# Gold set: phân loại issue (W1)

Nguồn: `data/evaluation/issue_classification_gold.json` (đọc-only, không sửa). Có 20 case.

## Các field

- `issue_id`: mã case, dạng CASE-01 đến CASE-20.
- `text`: nội dung issue, được thay vào `{issue_text}` trong prompt.
- `category`: một trong Bug, Feature, Question, Risk. Đây là gold label.
- `priority`: một trong P1, P2, P3. Đây là gold label.

## Danh sách case

| issue_id | text | category (gold) | priority (gold) |
|---|---|---|---|
| CASE-01 | Production checkout API down for all users | Bug | P1 |
| CASE-02 | Critical payment processing fails globally | Bug | P1 |
| CASE-03 | Data export returns 500 for all customers | Bug | P1 |
| CASE-04 | Passwords accepted but SSO blocks all logins | Bug | P1 |
| CASE-05 | Add download button to sprint chart | Feature | P3 |
| CASE-06 | Implement dark theme on PM dashboard | Feature | P3 |
| CASE-07 | Add a custom Jira field in status report | Feature | P2 |
| CASE-08 | Support export of reports as CSV | Feature | P3 |
| CASE-09 | What is the expected UAT deadline? | Question | P3 |
| CASE-10 | How many issues are in the current sprint? | Question | P3 |
| CASE-11 | Where are weekly release notes stored? | Question | P3 |
| CASE-12 | Who must approve an incident report? | Question | P2 |
| CASE-13 | Vendor API may miss December cutover | Risk | P2 |
| CASE-14 | Security certificate expires before go-live | Risk | P1 |
| CASE-15 | Single reviewer may delay UAT sign-off | Risk | P2 |
| CASE-16 | No fallback if external OAuth is down | Risk | P1 |
| CASE-17 | Sort order changes unexpectedly on issues page | Bug | P2 |
| CASE-18 | Change report frequency from weekly to daily | Feature | P2 |
| CASE-19 | Which region hosts our staging cluster? | Question | P3 |
| CASE-20 | Unreviewed dependencies could delay release | Risk | P2 |

## Thống kê

- Category: Bug 5, Feature 5, Question 5, Risk 5.
- Priority: P1 6, P2 7, P3 7.
- Case P1: CASE-01, CASE-02, CASE-03, CASE-04, CASE-14, CASE-16.
