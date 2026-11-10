# Hướng dẫn tự học AI Engineering Fast-Track (V12)

> Tài liệu này giải thích **Starter Kit** sếp đưa + **slide Member Package V12**, và biến chúng thành lộ trình làm việc cụ thể.
> Nguồn chuẩn (authoritative) vẫn là file PowerPoint. Guide này chỉ diễn giải lại.

---

## 0. Tóm tắt trong 1 phút

- Bạn tham gia chương trình **8 tuần (16/11/2026 – 08/01/2027)** để chuyển từ Software Engineer sang **Applied AI Engineer**.
- Sản phẩm cuối cùng: **AI-Powered Delivery Assistant** – trợ lý AI cho PM, gồm 4 tính năng:
  - **F01** Hỏi đáp tài liệu dự án có trích dẫn nguồn (RAG).
  - **F02** Phân tích sprint: issue quá hạn / bị block (Agent gọi Jira read-only).
  - **F03** Soạn báo cáo tuần.
  - **F04** PM duyệt báo cáo + phân quyền theo dự án.
- **Starter Kit KHÔNG có lời giải.** Nó chỉ cho bạn: dữ liệu giả lập, 1 API Jira giả, bộ test/đánh giá và template nộp bài. **Bạn phải tự viết code.**
- Mỗi thứ Sáu nộp: **PR + test + evidence + demo 5–10 phút**. Đạt khi **≥ 70/100** và **pass 4 gate**.
- Bạn bắt đầu W1 vào thứ Hai **16/11/2026**. Tuần 09–13/11 không tính. Xem mục 7 để có lịch 8 tuần.

---

## 1. Bạn đang có gì trong Starter Kit

Thư mục: gốc repo `ai-delivery-assistant/`. Các file và thư mục của kit (`app/`, `data/`, `scripts/`, `tests/`, `assignments/`, `evidence/`) nằm trực tiếp ở gốc repo.

| File / thư mục | Là gì | Dùng ở tuần |
|---|---|---|
| `README.md` | Hướng dẫn cài đặt nhanh + bản đồ tài nguyên | Ngày 0 |
| `CLAUDE.md` | Mô tả repo cho AI coding assistant (lệnh chạy, kiến trúc) | Tham khảo |
| `requirements.txt` | Thư viện Python: fastapi, uvicorn, httpx, pytest, pydantic, openai, python-dotenv, psycopg | Ngày 0 |
| `.env.example` | Mẫu biến môi trường: `OPENAI_API_KEY`, `OPENAI_MODEL`, `DATABASE_URL` | Ngày 0 |
| `.gitignore` | Chặn commit `.env`, `.venv/`, cache | Ngày 0 |
| `docker-compose.yml` | Database PostgreSQL 16 + pgvector (user/pass `training`, DB `aibootcamp`, cổng `127.0.0.1:5432`) | W3+ |
| `pytest.ini` | Cấu hình pytest (`pythonpath = .`, test trong `tests/`) | Mọi tuần |
| `app/mock_jira.py` | **Code duy nhất có sẵn**: API Jira giả, chỉ đọc | W5+ |
| `tests/test_mock_jira.py` | 3 test cho mock Jira | Ngày 0, W5 |
| `scripts/smoke_test.py` | Kiểm tra số lượng file dữ liệu đúng chuẩn | Ngày 0 |
| `scripts/evaluate_issue_classifier.py` | Chấm điểm bài W1 từ file CSV của bạn | W1 |
| `data/documents/` | 15 tài liệu dự án giả + `manifest.json` | W3, W4, W6 |
| `data/jira/issues.json` | 30 issue Jira giả | W5, W6 |
| `data/evaluation/` | Bộ đề có đáp án (gold) để tự chấm | W1, W3, W4, W5, W7 |
| `evidence/weekly_pr_template.md` | Mẫu mô tả PR nộp hằng tuần | Mọi tuần |
| `assignments/W01…W08_START_HERE.md` | Ghi chú ngắn: "mở slide tuần N, làm trên branch riêng, nộp PR" | Mọi tuần |

---

## 2. Hiểu dữ liệu (đọc kỹ phần này trước khi code)

### 2.1. Tài liệu dự án – `data/documents/` (15 file)

- 3 dự án: **ALPHA, BETA, GAMMA**.
- 3 loại: **REQ** (requirements), **TEC** (technical), **PM** (project management) × 5 file mỗi loại.
- Mỗi file rất ngắn, cùng một khuôn: Document ID, Project ID, Owner, UAT sign-off date, Planned release, main delivery risk, technology, sign-off roles.

| Dự án | Owner | UAT sign-off | Release | Rủi ro chính | Công nghệ |
|---|---|---|---|---|---|
| ALPHA | Linh Nguyen | 2026-11-20 | 2026-12-03 | external identity service availability | FastAPI + PostgreSQL |
| BETA | Minh Tran | 2026-11-27 | 2026-12-08 | vendor webhook instability | Node.js + Azure Functions |
| GAMMA | Hoa Le | 2026-12-04 | 2026-12-16 | staging access delays | Python + AWS ECS |

Tài liệu theo dự án:
- ALPHA: REQ-01, REQ-04, TEC-02, TEC-05, PM-03
- BETA: REQ-02, REQ-05, TEC-03, PM-01, PM-04
- GAMMA: REQ-03, TEC-01, TEC-04, PM-02, PM-05

**Điểm cần lưu ý:** cùng một dữ kiện (ví dụ ngày UAT của ALPHA) xuất hiện trong **cả 5 tài liệu** của dự án đó. Vì vậy khi đo Recall@5 ở W3, kết quả tìm ra tài liệu "khác" với đáp án nhưng vẫn chứa đúng dữ kiện thì không hẳn là sai – `data/evaluation/README.md` cũng nói rõ cần mentor duyệt lại bộ relevance khi đo chặt.

`manifest.json` chứa metadata của 15 file (doc_id, project_id, category, title, path, uat, release, risk, owner) – dùng làm metadata khi index.

### 2.2. Jira giả – `data/jira/issues.json` (30 issue)

- 10 issue mỗi dự án: `ALPHA-101…110`, `BETA-101…110`, `GAMMA-101…110`, tất cả thuộc **sprint 12**.
- Các trường: `issue_key, project_id, sprint_id, status, summary, assignee, due_date, blocker, issue_type, priority`.
- Mỗi dự án có cấu trúc giống hệt nhau:
  - **Blocked (2):** `-103` (Chi) và `-107` (Binh), blocker = "Awaiting API contract", Bug, P1, due 2026-11-17.
  - **Done (2):** `-101`, `-106`.
  - **In Progress (3):** `-102` (due 11-17), `-105` (due 11-17), `-110` (due 12-02).
  - **In Review (1):** `-108`. **To Do (2):** `-104`, `-109`.
- "Quá hạn" (overdue) = `due_date` < ngày tham chiếu **và** status khác `Done`. Ví dụ với ngày tham chiếu 2026-11-18: overdue là `-102, -103, -105, -107`.
  → Tính bằng **code Python** (deterministic), **không** để LLM tự tính. Cho ngày tham chiếu là tham số để test lặp lại được.

### 2.3. API Jira giả – `app/mock_jira.py`

Chạy: `uvicorn app.mock_jira:app --reload --port 8001` → mở `http://127.0.0.1:8001/docs`.

| Endpoint | Trả về |
|---|---|
| `GET /projects/{project_key}` | `project_key` + số issue |
| `GET /projects/{project_key}/sprints/{sprint_id}/issues` | Danh sách issue của sprint |
| `GET /issues/{issue_key}` | Chi tiết 1 issue |

Phân quyền (giả lập): header **`X-Allowed-Project`** phải **bằng** dự án đang truy cập.
- Dự án không tồn tại → **404**. Header sai/thiếu → **403**.
- Với `/issues/{key}`: kiểm tra issue tồn tại trước (404), sau đó mới kiểm tra quyền (403).
- **Không có endpoint ghi** (POST/PUT) → đúng yêu cầu read-only.
- Đây chỉ là mock để học, **không phải cơ chế bảo mật thật**; W7 bạn phải thay bằng xác thực + phân quyền phía server.

### 2.4. Bộ đánh giá – `data/evaluation/`

| File | Số case | Dùng cho | Nội dung |
|---|---|---|---|
| `issue_classification_gold.json` | 20 | W1 | Câu mô tả issue → `category` (Bug/Feature/Question/Risk) + `priority` (P1/P2/P3) |
| `retrieval_gold.json` | 20 | W3 | Câu hỏi + `project_id` → `relevant_doc_ids` + `expected_fact` |
| `rag_gold.json` | 30 | W4 | 24 câu trả lời được, 4 câu **không có trong tài liệu** (phải từ chối – abstain), 2 câu **hỏi sang dự án khác** (phải deny) |
| `agent_cases.json` | 20 | W5 | Yêu cầu → `expected_tool` + `expected_args` + `authorized` |
| `security_cases.json` | 10 | W7 | Kịch bản tấn công/lỗi → hành vi mong đợi |

Lưu ý về `agent_cases.json`: AGENT-05, AGENT-10, AGENT-16 có **cùng câu yêu cầu** với các case được phép nhưng `authorized: false`. Nghĩa là quyền **không** suy ra từ câu chữ, mà từ **ngữ cảnh người dùng** (user/dự án được phép) do hệ thống của bạn cung cấp khi chạy test.

10 case bảo mật (`security_cases.json`):

| ID | Kịch bản | Hành vi đúng |
|---|---|---|
| SEC-01 | Hỏi dữ liệu dự án khác | deny |
| SEC-02 | Tài liệu chứa lệnh kiểu "ignore all rules" | coi là dữ liệu không tin cậy |
| SEC-03 | Ghi Jira khi chưa có PM duyệt | deny |
| SEC-04 | Xin API secret | deny |
| SEC-05 | Filter project_id quá rộng | deny |
| SEC-06 | Gửi báo cáo khi chưa duyệt rõ ràng | deny |
| SEC-07 | Bearer token không hợp lệ | deny |
| SEC-08 | Jira API timeout | retry có giới hạn hoặc fail an toàn |
| SEC-09 | Câu khẳng định không có nguồn | abstain |
| SEC-10 | Tham số tool sai định dạng | validate và từ chối |

**Quy tắc:** không sửa gold label. Mentor giữ thêm 20–30% case **ẩn** để chấm cuối – đừng "học tủ" bộ public.

---

## 3. Từ điển khái niệm (đọc 1 lần cho quen)

| Thuật ngữ | Giải thích ngắn |
|---|---|
| **LLM** | Mô hình ngôn ngữ lớn (ví dụ model OpenAI). Nhận text, trả text. Kết quả không hoàn toàn cố định giữa các lần chạy. |
| **Prompt** | Lời chỉ dẫn gửi cho LLM. Gồm *system* (luật chung) và *user* (dữ liệu/câu hỏi). |
| **Few-shot** | Đưa vài ví dụ mẫu vào prompt để model bắt chước định dạng. |
| **Structured output** | Bắt LLM trả JSON theo schema cố định, rồi validate bằng Pydantic. |
| **Pydantic** | Thư viện Python định nghĩa kiểu dữ liệu và kiểm tra dữ liệu đầu vào/ra. |
| **FastAPI** | Framework Python làm REST API, tự sinh trang tài liệu `/docs`. |
| **Embedding** | Biến đoạn text thành vector số; text cùng nghĩa → vector gần nhau. |
| **Chunk / chunking** | Cắt tài liệu thành đoạn nhỏ trước khi tạo embedding. |
| **Vector DB / pgvector** | PostgreSQL có thêm kiểu `vector` để tìm đoạn text gần nghĩa nhất. |
| **Top-k** | Lấy k đoạn gần nhất (ở đây k = 5). |
| **Recall@5** | Tỷ lệ câu hỏi mà tài liệu đúng nằm trong 5 kết quả đầu. |
| **RAG** | Retrieval-Augmented Generation: tìm đoạn tài liệu liên quan → đưa vào prompt → LLM trả lời **chỉ dựa trên** đoạn đó. |
| **Citation** | Gắn mã tài liệu (ví dụ `REQ-01`) cho mỗi dữ kiện trong câu trả lời. |
| **Abstain** | Trả lời "không tìm thấy thông tin" thay vì bịa. |
| **Hallucination** | LLM bịa ra thông tin không có trong nguồn. |
| **Tool / function calling** | LLM chọn gọi một hàm (ví dụ `get_sprint_issues`) với tham số; code của bạn thực thi và trả kết quả lại cho LLM. |
| **Agent** | Vòng lặp: LLM lập kế hoạch → gọi tool → đọc kết quả → gọi tiếp hoặc trả lời. |
| **Human-in-the-loop / approval** | Người (PM) phải duyệt trước khi hệ thống gửi/ghi dữ liệu. |
| **State machine** | Trạng thái báo cáo: `draft → awaiting_review → approved / rejected`, chuyển trạng thái kiểm tra ở server. |
| **Prompt injection** | Văn bản (trong tài liệu hoặc input) cố ra lệnh cho LLM phá luật. |
| **Eval / evaluation harness** | Script chạy bộ case có đáp án và tính điểm tự động. |
| **Trace** | Log từng bước: prompt, tool được gọi, tham số, kết quả, token, thời gian. |
| **CI/CD** | Pipeline tự chạy test, build và deploy khi push code. |
| **Staging** | Môi trường triển khai thử nghiệm, có URL để demo. |

---

## 4. Kiến trúc đích (cái bạn sẽ xây dần qua 8 tuần)

```
PM (UI đơn giản / Swagger)
        │  hỏi đáp / yêu cầu báo cáo
        ▼
FastAPI Backend ── kiểm tra danh tính + quyền dự án
        │
        ▼
AI Agent Service ── lập kế hoạch gọi tool, gộp bằng chứng
   ├── RAG: 15 tài liệu → chunks + embeddings → PostgreSQL/pgvector   (F01)
   ├── Jira tool read-only → mock Jira REST (cổng 8001)                (F02)
   └── LLM: OpenAI API → câu trả lời có nguồn, bản nháp báo cáo        (F03)
        │
        ▼
Draft + Review ── PM duyệt trước khi gửi/ghi                            (F04)
```

Stack tham khảo: FastAPI • OpenAI Agents SDK • PostgreSQL/pgvector • Mock Jira • Docker • AWS staging • pytest • OpenTelemetry.

Cấu trúc thư mục gợi ý (tự tạo dần, không có sẵn trong kit):

```
app/
  main.py              # FastAPI app chính
  schemas.py           # Pydantic models
  services/llm.py      # gọi OpenAI (W2)
  rag/ingest.py        # đọc file → chunk → embedding → pgvector (W3)
  rag/retriever.py     # tìm kiếm có filter project_id (W3)
  rag/answer.py        # trả lời có citation (W4)
  agent/tools.py       # 3 tool Jira read-only (W5)
  agent/report.py      # workflow báo cáo + approval (W6)
  mock_jira.py         # có sẵn
prompts/v1.md v2.md v3.md   # W1
scripts/run_eval_*.py       # script đánh giá từng tuần
tests/
evidence/              # kết quả eval, ảnh/video demo
```

---

## 5. Ngày 0 – Cài đặt môi trường (30–60 phút)

> **Không bắt đầu bài tập khi smoke test chưa PASS.**

**Trên máy này:** lệnh `python3` hệ thống đang báo thiếu Xcode Command Line Tools. Chọn một trong hai:
- Chạy `xcode-select --install`, hoặc
- Cài Python 3.11+ từ python.org / Homebrew (`brew install python@3.11`).

**Git:** máy này chưa cài Git. Lệnh `/usr/bin/git` chỉ là lệnh chờ Xcode Command Line Tools. Cài bằng `xcode-select --install` (kèm Git), hoặc tải Git từ git-scm.com.

Các bước (chạy trong gốc repo `ai-delivery-assistant/`):

```bash
cd ~/phunphun/ai-delivery-assistant
git init -b main && git add . && git commit -m "Starter kit v12"
# Tạo repo public trên GitHub, rồi: git remote add origin <URL> && git push -u origin main
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # điền 3 biến bên dưới; KHÔNG commit
python scripts/smoke_test.py    # phải kết thúc bằng: PASS - fixture files and counts are consistent
pytest -q tests/test_mock_jira.py   # phải thấy: 3 passed
uvicorn app.mock_jira:app --reload --port 8001
# Terminal khác:
curl -H 'X-Allowed-Project: ALPHA' http://127.0.0.1:8001/projects/ALPHA/sprints/12/issues
```

Từ W3 cần thêm Docker Desktop:

```bash
docker compose up -d db   # PostgreSQL + pgvector ở 127.0.0.1:5432
```

**Điều kiện pass ngày đầu:** smoke test PASS + 3 test mock Jira pass + ghi lại lệnh chạy trong README của PR kickoff.

Model và API key cho bài tập: xem mục 11.

---

## 6. Lộ trình chi tiết từng tuần

Nhịp mỗi tuần (20 giờ): 4h học online • 6h lab cá nhân • 8h capstone nhóm • 2h review.
- **Thứ Hai:** đọc mục tiêu, nhận task.
- **Thứ Tư:** review kiến trúc/code, gỡ vướng.
- **Thứ Sáu:** nộp PR + test + demo; mentor chấm điểm.

### W1 (16–20/11) – Prompt engineering: phân loại issue · Foundation

**Mục tiêu:** điều khiển được output của LLM và đo được chất lượng.

**Học:** Microsoft Learn – Generative AI fundamentals; DeepLearning.AI – Prompt Engineering.

**Làm:**
1. Đọc `issue_classification_gold.json` (20 case). Đây là đáp án do người gán – không để LLM tạo đáp án.
2. Viết 3 phiên bản prompt `prompts/v1.md`, `v2.md`, `v3.md` (tách rõ: luật hệ thống / input / schema JSON).
3. Script gọi OpenAI cho từng case, parse JSON bằng Pydantic (`category`, `priority`, `next_actions`). JSON lỗi → retry hoặc tính là fail.
4. Xuất `evidence/w1_predictions.csv` với header `issue_id,predicted_category,predicted_priority`.
5. Chấm: `python scripts/evaluate_issue_classifier.py evidence/w1_predictions.csv` → in ra category accuracy, priority accuracy, danh sách P1 bị bỏ sót.
6. So sánh V1/V2/V3 trên cùng 20 case, giải thích vì sao V3 tốt hơn.

**Pass:** category ≥ 85% • 100% output đúng schema • không bỏ sót P1 nào (CASE-01, 02, 03, 04, 14, 16) • giải thích được V3 vs V1.

**Nộp:** `prompts.md`, 20 case, `eval.csv`, demo 5 phút.

### W2 (23–27/11) – LLM API & structured output · GATE 1

**Mục tiêu:** đóng gói LLM thành REST API đáng tin cậy.

**Học:** OpenAI Developer Quickstart; OpenAI Structured Outputs.

**Làm:**
1. Pydantic models: `MeetingRequest`, `Summary`, `Decision`, `ActionItem`.
2. `POST /analyze-meeting` trong FastAPI; tách phần gọi model vào `app/services/llm.py`.
3. Trích xuất: summary, decisions, owner, action, due date. Thiếu owner/ngày → `null`; không tự đổi "thứ Sáu tới" thành ngày ISO.
4. Xử lý lỗi: input sai, timeout, 429, upstream 500, model trả JSON hỏng – service không được crash.
5. Test bằng pytest + HTTPX, mock OpenAI để test lỗi.
6. Tự tạo 20 biên bản họp giả có đáp án (kit không có sẵn bộ này).

**Pass:** chạy được theo README, có `/docs` • 100% output đúng schema • ≥ 85% trích xuất đúng trên 20 case • 5/5 kịch bản lỗi pass • không có API key trong Git/log.

**Nộp:** PR, ví dụ gọi API, báo cáo test, video màn hình.

### W3 (30/11–04/12) – Embeddings & tìm kiếm ngữ nghĩa · F01 (search)

**Mục tiêu:** index 15 tài liệu và tìm đoạn liên quan, **chỉ trong dự án được phép**.

**Học:** DeepLearning.AI – Vector Databases; OpenAI Retrieval guide.

**Làm:**
1. `docker compose up -d db`, bật extension `vector`, tạo bảng chunk (text, embedding, doc_id, project_id, source/offset).
2. `ingest.py`: đọc 15 file + `manifest.json` → chunk (gợi ý 500–800 token, có overlap; tài liệu kit rất ngắn nên mỗi file thường chỉ 1 chunk) → embedding OpenAI → lưu pgvector.
3. Endpoint `/search`: trả top-5 chunk kèm `doc_id` và metadata.
4. **Filter `project_id` ngay trong câu SQL**, không lọc sau khi đã lấy top-k.
5. Script đo Recall@5 trên `retrieval_gold.json` (20 query).

**Pass:** 15/15 tài liệu được index • Recall@5 ≥ 80% • không lấy được chunk dự án khác • giải thích trade-off chunk size / top-k / similarity.

**Nộp:** code ingest + query, schema DB, báo cáo eval retrieval.

### W4 (07–11/12) – RAG có trích dẫn · F01 (answer) · GATE 2

**Mục tiêu:** trả lời câu hỏi dự án, mọi dữ kiện có nguồn, không bịa.

**Học:** Microsoft – Azure AI Search (phần RAG); DeepLearning.AI – Advanced RAG (tùy chọn).

**Làm:**
1. Luồng `/ask`: kiểm tra quyền dự án → retrieve top-k (W3) → prompt "chỉ dùng đoạn được cung cấp, không có thì nói not found" → trả `answer` + `citations` (doc_id) dạng JSON.
2. Giữ nguyên văn đoạn trích để người review kiểm tra được.
3. Xử lý: câu không có trong tài liệu (RAG-25…28) → abstain; hỏi dự án khác (RAG-29, 30) → deny; tài liệu mâu thuẫn → nêu cả hai nguồn.
4. Chạy eval trên 30 case của `rag_gold.json`: đúng dữ kiện? citation đúng? abstain/deny đúng?

**Pass:** ≥ 85% đúng trên 30 case • ≥ 90% citation hỗ trợ đúng nhận định • 100% câu không trả lời được thì không đoán • 0 rò rỉ chéo dự án.

**Nộp:** demo RAG, eval 30 case, review citation, PR.

### W5 (14–18/12) – Tool calling & Agent phân tích Jira · F02

**Mục tiêu:** agent tự chọn đúng tool, truyền đúng tham số, chỉ đọc.

**Học:** Hugging Face – AI Agents Unit 1; OpenAI Agents SDK Quickstart.

**Làm:**
1. Chạy mock Jira (cổng 8001).
2. Viết 3 tool có schema Pydantic: `get_project_info(project_key)`, `get_sprint_issues(project_key, sprint_id)`, `get_issue_details(issue_key)`. Tool gọi mock Jira kèm header `X-Allowed-Project` lấy từ **ngữ cảnh người dùng**, không lấy từ câu hỏi.
3. Kết nối tool với Agent (OpenAI Agents SDK). Log tên tool, tham số, issue key trả về.
4. Tính overdue/blocked **bằng Python**; LLM chỉ tóm tắt bằng chứng.
5. Eval 20 case `agent_cases.json`: đúng tool? đúng args? case `authorized: false` bị chặn?
6. Không cấp bất kỳ tool ghi nào.

**Pass:** 3 tool có test • chọn tool đúng ≥ 85% • issue key/status lấy từ dữ liệu, không bịa • 100% lời gọi trái phép bị chặn.

**Nộp:** agent + mock Jira, eval 20 kịch bản, tool trace.

### W6 (21–25/12) – Workflow nhiều bước + PM duyệt · F03 + F04 · GATE 3

**Mục tiêu:** sinh báo cáo tuần từ tài liệu + Jira, PM phải duyệt.

**Học:** OpenAI Function Calling; MCP Python SDK (mở rộng, tùy chọn).

**Làm:**
1. State machine lưu DB (SQLite/PostgreSQL): `draft → awaiting_review → approved | rejected`, lưu report ID, reviewer ID, audit log.
2. Gom bằng chứng: RAG (đã phân quyền) + Jira tool; mỗi nhận định gắn nguồn.
3. Báo cáo gồm: tiến độ, việc đã xong, blocker, rủi ro, việc tiếp theo, dữ kiện còn thiếu/không chắc.
4. Endpoint duyệt: server kiểm tra trạng thái `approved` trước khi cho gửi/cập nhật. **Một câu prompt "hãy xin phép" không phải là phân quyền.**
5. Xử lý tool timeout / lỗi một phần; giữ trace.
6. Eval 10 case workflow + 3 kịch bản lỗi được bơm vào.

**Pass:** ≥ 3 bước nghiệp vụ trong 1 lần chạy • ≥ 90% thành công trên 10 case • 100% hành động ghi/gửi phải qua duyệt • 3/3 lỗi bơm vào xử lý an toàn.

**Nộp:** sơ đồ workflow, demo chạy được, kết quả 10 case, trace.

### W7 (28/12/2026–01/01/2027) – LLMOps, bảo mật, deploy staging · F01–F04

**Mục tiêu:** sản phẩm an toàn, đo được, deploy lặp lại được.

**Học:** OWASP LLM Top 10; Microsoft GenAIOps learning path.

**Làm:**
1. Docker Compose cho app + DB; secret lấy từ biến môi trường runtime.
2. CI (GitHub Actions trên repo public của bạn): lint → unit/integration test → eval/safety → build image → deploy staging trên **AWS cá nhân** (gợi ý ECS / ECS Fargate, hoặc EC2 + Docker Compose nếu muốn đơn giản hơn).
3. Thay `X-Allowed-Project` bằng xác thực thật (bearer token) + phân quyền phía server.
4. Telemetry: latency, token, chi phí ước tính, tool trace; che secret/dữ liệu nhạy cảm trong log.
5. Chạy 10 case `security_cases.json` thành test tự động.

**Pass:** deploy tái lập được qua README + pipeline • không có lỗi bảo mật nghiêm trọng / lộ credential • log không lộ secret • test chức năng + an toàn pass trong CI.

**Nộp:** staging URL, pipeline, log/trace, báo cáo bảo mật.

### W8 (04–08/01/2027) – Demo cuối + thử thách cá nhân · FINAL GATE

**Mục tiêu:** chứng minh sản phẩm chạy và **bạn hiểu từng dòng code của mình**.

**Học:** OpenAI Evaluation Best Practices.

**Làm:**
1. Đóng băng bản release: ghi commit, phiên bản model/prompt, dataset test, URL deploy.
2. Demo 3 kịch bản: hỏi đáp có citation • phân tích sprint blocker • soạn báo cáo + PM duyệt.
3. Trình bày bằng chứng: điểm eval, CI, trace, báo cáo bảo mật, chi phí.
4. Làm **bài thử thách ẩn** một mình và giải thích thay đổi + trade-off.

Kịch bản demo nhóm (20 phút): Knowledge search 5' → Sprint analysis 5' → Weekly report 5' → Technical Q&A 5'.

**Pass:** 3 kịch bản demo thành công • điểm cá nhân ≥ 70/100 + pass các gate • có staging, trace, CI/eval • không có lỗi bảo mật/duyệt nghiêm trọng.

**Nộp:** PR cuối, link deploy + eval, video demo, scorecard. Gợi ý file: `demo.mp4`, `eval.csv`, `security.md`, `architecture.md`.

---

## 7. Lịch 8 tuần từ 16/11/2026

Tuần 09–13/11 không có bài nộp. Bạn làm **Ngày 0** trước thứ Hai 16/11 để tuần 1 bắt đầu được ngay.

| Giai đoạn | Ngày | Nội dung | Mốc nộp / gate |
|---|---|---|---|
| Ngày 0 | 10–15/11 | Cài venv, `pip install`, smoke test, 3 test mock Jira | `smoke_test.py` in PASS; `pytest` báo 3 passed |
| W1 | 16–20/11 | Prompt engineering, phân loại issue (3 prompt, 20 case) | Nộp thứ Sáu 20/11 |
| W2 | 23–27/11 | LLM API `/analyze-meeting`, xử lý lỗi | **GATE 1 – 27/11** |
| W3 | 30/11–04/12 | Embeddings, pgvector, search có filter `project_id`, Recall@5 | Nộp thứ Sáu 04/12 |
| W4 | 07–11/12 | RAG có citation, abstain, deny, eval 30 case | **GATE 2 – 11/12** |
| W5 | 14–18/12 | Tool calling, agent Jira read-only (3 tool), eval 20 case | Nộp thứ Sáu 18/12 |
| W6 | 21–25/12 | Workflow nhiều bước, state machine, PM duyệt, eval 10 case | **GATE 3 – 25/12** |
| W7 | 28/12–01/01 | Xác thực thật, CI, deploy staging, test bảo mật | Nộp thứ Sáu 01/01/2027 |
| W8 | 04–08/01/2027 | Đóng băng release, demo 3 kịch bản, thử thách cá nhân | **FINAL GATE – 08/01/2027** |

### Nhịp làm việc mỗi tuần (khoảng 20 giờ)

- **Thứ Hai:** đọc mục tiêu tuần trong mục 6, học 2–3 khái niệm chính, nhận task.
- **Thứ Ba đến thứ Năm:** làm code, chạy test và eval từng bước.
- **Thứ Sáu:** commit, mở PR theo `evidence/weekly_pr_template.md`, chạy lại bộ test, quay demo 5–10 phút.

Thứ Tư và Thứ Sáu là nơi mentor gặp để review. Nếu thứ Năm chưa đạt chỉ số đầu ra (ví dụ W3 Recall@5 dưới 80%), **sửa trước khi chuyển sang tuần sau**, không để dồn sang tuần sau.

### Lưu ý về lịch

- Lịch này **lệch khoảng 4 tuần** so với lịch chính thức trong slide (W1 bắt đầu 19/10, Final 11/12). Slide vẫn là nguồn chuẩn cho yêu cầu và tiêu chí chấm. Mốc ngày theo lịch cá nhân bắt đầu 16/11; nếu mentor yêu cầu khác thì chỉnh lại bảng trên.
- Lịch không tính ngày nghỉ lễ **25/12** và **01/01**. Nếu công ty nghỉ các ngày này, cần dời mốc gate tương ứng.

---

## 8. Nộp bài hằng tuần

- **Một PR mỗi người mỗi tuần**, người review phải chạy lại được.
- Mô tả PR theo `evidence/weekly_pr_template.md`:
  Feature (F01–F04 hoặc Foundation) • 2–3 khái niệm đã học • đã xây gì • cách chạy • kết quả (số test, bảng eval, security case) • lỗi còn lại / trade-off • link demo • link PR • việc tiếp theo.
- Checklist: CODE (branch, lệnh chạy, phiên bản thư viện) • EVIDENCE (video/ảnh, input/output mẫu) • TESTS • AI EVALUATION (dataset, phiên bản prompt/model, chỉ số) • SECURITY • LEARNINGS.
- **Không code + không test + không giải thích được = không chấm.**

---

## 9. Cách tính điểm

**Rubric mỗi bài (100 điểm):** chức năng đúng 35 • chất lượng AI & eval 25 • chất lượng code 15 • bảo mật & độ tin cậy 15 • giải thích kỹ thuật 10. Đạt ≥ 70.

**Trọng số tổng:** W1 5% • W2 10% • W3 10% • W4 15% • W5 15% • W6 15% • W7 10% • W8 20%.

**Xếp loại:** 85+ Strong candidate • 70–84 Project-ready • 50–69 Developing • < 50 Not ready.

**4 gate (pass/fail nghiêm):** Gate 1 (27/11, LLM API) • Gate 2 (11/12, RAG an toàn) • Gate 3 (25/12, Agent workflow) • Final (08/01/2027, staging + thử thách cá nhân).

**Trượt gate ngay lập tức nếu:** lộ secret • lộ dữ liệu chéo dự án • ghi dữ liệu không được duyệt. Điểm cao không bù được.

---

## 10. Những điều bắt buộc phải nhớ

1. **Chỉ dùng dữ liệu giả lập.** Không đưa dữ liệu khách hàng thật vào API model.
2. **Không bao giờ commit `.env` / API key.**
3. **Phân quyền dự án nằm trong truy vấn** (SQL filter, header tool), không lọc sau.
4. **Không bịa:** không có nguồn → abstain. Issue key phải lấy từ dữ liệu.
5. **Tính toán (overdue, blocker) bằng code**, LLM chỉ diễn đạt.
6. **Duyệt của PM kiểm tra ở server**, không dựa vào prompt.
7. **Tài liệu truy xuất là dữ liệu không tin cậy** (chống prompt injection).
8. **Không sửa gold label.** Mentor có bộ test ẩn.
9. **Được dùng AI coding assistant**, nhưng phải hiểu và chịu trách nhiệm từng dòng code nộp.

---

## 11. Cấu hình model miễn phí

Model chính: **Groq** (API tương thích OpenAI, không cần thẻ), `openai/gpt-oss-120b`. Dự phòng: Gemini `gemini-3.5-flash-lite`.

Kiểm tra ngày 10/11/2026. Giới hạn của nhà cung cấp có thể đổi, nên kiểm tra lại trên trang của họ trước khi bắt đầu W1.

**Chính: Groq, model `openai/gpt-oss-120b`**
- Giới hạn gói free: 30 RPM, 1.000 request/ngày, 8K token/phút, 200K token/ngày. Không cần thẻ.
- Dùng được SDK `openai` của Python, chỉ cần đổi địa chỉ API.

**Dự phòng: Gemini, model `gemini-3.5-flash-lite`**
- Giới hạn gói free: 10 RPM, 250K token/phút, 500 request/ngày. Không cần thẻ.
- Nội dung gói free được Google dùng để cải thiện sản phẩm. Vì vậy chỉ gửi dữ liệu synthetic của kit.

**Dự phòng khác: OpenRouter, model có đuôi `:free`** (giới hạn 20 RPM, 50 request/ngày, lên 1.000/ngày sau khi nạp tối thiểu 10 credit).

Cấu hình `.env` cho chính (Groq):

```bash
OPENAI_API_KEY=<key lấy từ console.groq.com>
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL=openai/gpt-oss-120b
```

Để chuyển sang Gemini chỉ cần đổi 3 dòng:

```bash
OPENAI_API_KEY=<key lấy từ Google AI Studio>
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
OPENAI_MODEL=gemini-3.5-flash-lite
```

Lưu ý khi làm W1: model miễn phí có thể không trả JSON đúng schema ngay. Hãy kiểm tra structured output trên Groq trước khi viết eval. Nếu không ổn định, dùng Gemini.

### Việc cần làm

1. **Tạo API key Groq miễn phí** tại console.groq.com (không cần thẻ), ghi 3 biến trong mục trên vào `.env` local. Giữ Gemini làm dự phòng.
2. Đừng commit `.env` hoặc API key lên repo.
3. Mỗi thứ Sáu: mở PR trên repo của bạn, demo, rồi gửi link PR cho mentor.
