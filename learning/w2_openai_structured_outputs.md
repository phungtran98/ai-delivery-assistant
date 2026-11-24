# W2 – Ghi chú học: OpenAI Quickstart và Structured Outputs

**Nguồn:**
- OpenAI Developer Quickstart: https://developers.openai.com/api/docs/quickstart
- OpenAI Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs

**Mục tiêu đọc:** hiểu cách gọi API, cách ép output theo JSON schema, và các trường hợp model không trả được output hợp lệ.

---

## Phần 1. Quickstart: gọi API lần đầu

### 1.1. Bước 1 – Tạo API key

- Tạo API key trong dashboard của OpenAI. Docs yêu cầu lưu key ở nơi an toàn.
- Không dán key vào chat, không đưa key vào code, không commit key lên Git.

### 1.2. Bước 2 – Đưa key vào biến môi trường `OPENAI_API_KEY`

Docs đưa hai lệnh, tùy hệ điều hành:

```bash
# macOS / Linux
export OPENAI_API_KEY="your_api_key_here"
```

```powershell
# Windows PowerShell
setx OPENAI_API_KEY "your_api_key_here"
```

Docs gợi ý lưu key vào file như `.zshrc` để không phải export lại mỗi lần mở terminal. Điều này có nghĩa là:
- `export` chỉ có tác dụng trong terminal đang mở.
- Muốn giữ lâu dài, bạn ghi lệnh `export` vào file cấu hình của shell (ví dụ `.zshrc`).

### 1.3. Bước 3 – SDK tự đọc key từ môi trường

Docs ghi: mỗi SDK tự đọc API key từ biến môi trường. Mình đã kiểm tra mã nguồn `openai` phiên bản 2.48.0 trên PyPI: SDK gọi `os.environ.get("OPENAI_API_KEY")` và `os.environ.get("OPENAI_BASE_URL")`. Vì vậy:
- Bạn không cần truyền key vào `OpenAI(...)`.
- Bạn cũng có thể đặt `OPENAI_BASE_URL` trong môi trường để SDK gọi provider khác (ví dụ Groq).

### 1.4. Cách repo này dùng: file `.env`

Trong repo, key và cấu hình nằm trong `.env`, không phải trong `.zshrc`:
- `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`.
- `scripts/classify_one.py` gọi `load_dotenv(root / ".env")`. Hàm này đưa các biến trong `.env` vào môi trường của tiến trình Python, nên SDK đọc được.
- `export` trong terminal không tự đọc `.env`. Chỉ code có gọi `load_dotenv` mới đọc file này.
- `.env` nằm trong `.gitignore`, nên không bị commit.

**Tóm tắt để nhớ:** key là bí mật. Nó nằm ngoài code và ngoài Git. Code chỉ đọc key từ môi trường.

### 1.5. Bước 4 – Cài SDK và gọi một request đầu tiên

Docs Python: cài SDK bằng pip, tạo file `example.py`, chạy `python example.py`.

```bash
pip install openai
```

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-6.2-astra",
    input="Write a one-sentence bedtime story about a unicorn.",
)

print(response.output_text)
```

Ba điểm cần nhớ:

| Thành phần | Ý nghĩa |
|---|---|
| `OpenAI()` | Tạo client. Client đọc key từ môi trường. |
| `client.responses.create(...)` | Gọi Responses API. |
| `model=` | Tên model. Trang docs dùng `gpt-6.2-astra` làm ví dụ. Trong project, bạn dùng model ghi trong `.env` (`OPENAI_MODEL`). |
| `input=` | Nội dung gửi cho model. |
| `response.output_text` | Chuỗi text model trả về. |

**Lưu ý về model:** tên `gpt-6.2-astra` chỉ là ví dụ của trang docs. Provider và model của W2 vẫn đang chờ bạn chốt (xem `timeline_checklist/w2.md`).

### 1.6. Hai API trong trang này

Quickstart dùng **Responses API** (`client.responses.create`). W1 của bạn dùng **Chat Completions API** (`client.chat.completions.create`) trong `scripts/classify_one.py`. Trang Structured Outputs ghi rõ cả hai API đều hỗ trợ Structured Outputs. Vì vậy hai cách này đều đúng, nhưng cú pháp khác nhau.

---

## Phần 2. Structured Outputs: ép output theo schema

### 2.1. Vấn đề cần giải

JSON là định dạng phổ biến để các ứng dụng trao đổi dữ liệu. Nếu bạn chỉ yêu cầu "trả JSON" trong prompt, model có thể:
- trả JSON thiếu trường,
- đổi tên trường,
- trả enum không nằm trong danh sách,
- hoặc trả text ngoài JSON.

**Structured Outputs** ràng buộc output của model theo JSON Schema bạn cung cấp. Trang docs nói rõ: ràng buộc này áp dụng cho output đã hoàn thành và không phải refusal.

### 2.2. Ba lợi ích theo docs

1. **Tuân thủ schema:** trường bắt buộc và giá trị enum theo đúng schema.
2. **Refusal rõ ràng:** việc model từ chối vì lý do an toàn có thể được kiểm tra bằng code.
3. **Prompt đơn giản hơn:** không cần prompt nhấn mạnh "hãy trả đúng format".

### 2.3. Quan trọng: schema không thay thế kiểm tra của bạn

Docs ghi: ứng dụng vẫn phải xử lý refusal, output chưa hoàn thành, lỗi API, và kiểm tra các quy tắc nghiệp vụ mà schema không diễn đạt được.

**Ví dụ:** schema bảo đảm `due_date` là chuỗi. Schema không biết "thứ Sáu tới" có phải ngày hợp lệ hay không. Bạn phải kiểm tra điều đó trong code hoặc trong prompt.

### 2.4. Cách 1 – Pydantic (Python)

Trang docs cho Python dùng `pydantic.BaseModel` để định nghĩa schema:

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    model="gpt-6.2-astra",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

event = response.output_parsed
```

- `text_format=CalendarEvent`: SDK biến class Pydantic thành JSON schema.
- `response.output_parsed`: object Pydantic đã parse sẵn.

### 2.5. Cách 2 – JSON schema thô (`text.format`)

Đây là cách trang Step 2 dùng để giải thích. Cú pháp:

```python
response = client.responses.create(
    model="gpt-6.2-astra",
    input=[
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"},
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "math_response",
            "schema": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": {"type": "string"},
                                "output": {"type": "string"},
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": False,
                        },
                    },
                    "final_answer": {"type": "string"},
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
)

print(response.output_text)
```

Các trường cần nhớ:

| Trường | Ý nghĩa |
|---|---|
| `type: "json_schema"` | Bật Structured Outputs. |
| `name` | Tên schema. |
| `schema` | JSON Schema bạn muốn model tuân theo. |
| `strict: True` | Bật ràng buộc schema nghiêm ngặt. |

Ví dụ docs luôn đặt `"additionalProperties": False` ở mọi object, và liệt kê mọi trường trong `required`. Docs dùng cách này trong ví dụ. Tài liệu không nêu đây là quy tắc bắt buộc trong phần này, nên hãy đọc lại mục "Supported schemas" khi viết schema thật.

**Lưu ý về độ trễ:** lần đầu gọi với một schema mới sẽ chậm hơn. Các lần sau với cùng schema không chậm thêm.

### 2.6. Mẹo viết schema (theo docs)

- Đặt tên trường rõ ràng, trực quan.
- Thêm `title` và `description` cho các trường quan trọng.
- Dùng evals để chọn cấu trúc nào hoạt động tốt nhất cho use case của bạn.

---

## Phần 3. Các loại schema được hỗ trợ

Structured Outputs hỗ trợ một tập con của JSON Schema:

**Kiểu dữ liệu:** `string`, `number`, `boolean`, `integer`, `object`, `array`, `enum`, `anyOf`.

**Ràng buộc có thể dùng:**
- `string`: `pattern` (regex), `format` (ví dụ `date`, `date-time`, `email`, `uuid`).
- `number`: `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `multipleOf`.
- `array`: `minItems`, `maxItems`.

**Quy tắc quan trọng:** object gốc (root) phải là `object`, không được là `anyOf`. Một discriminated union vẫn dùng được bên trong object, nhưng không dùng được ở gốc.

Ví dụ: schema gốc `anyOf` (phát sinh khi dùng `z.discriminatedUnion` trong Zod) bị API từ chối. Đưa union vào trong một trường của object thì được.

---

## Phần 4. Ba trường hợp model không trả output hợp lệ

Trang Step 3 nêu rõ: model có thể không trả output khớp schema trong ba trường hợp chính:

1. **Refusal:** model từ chối vì lý do an toàn.
2. **Incomplete, `max_output_tokens`:** output bị cắt vì chạm giới hạn token.
3. **Incomplete, `content_filter`:** output bị dừng bởi bộ lọc nội dung.

### 4.1. Cách kiểm tra (Python, theo docs)

```python
try:
    response = client.responses.create(
        model="gpt-6.2-astra",
        input=[...],          # như ví dụ trên
        text={"format": {...}},  # schema như ví dụ trên
        max_output_tokens=1024,
    )

    if (
        response.status == "incomplete"
        and response.incomplete_details.reason == "max_output_tokens"
    ):
        raise Exception("Incomplete response")

    message = next((item for item in response.output if item.type == "message"), None)
    math_response = message.content[0] if message and message.content else None

    if not math_response:
        raise Exception("No response content")

    if math_response.type == "refusal":
        print(math_response.refusal)
    elif math_response.type == "output_text":
        print(math_response.text)
    else:
        raise Exception("No response content")
except Exception as e:
    print(e)
```

**Điểm cần hiểu:**
- Kiểm tra `response.status` trước, rồi mới đọc nội dung.
- Nội dung của message có thể là `refusal` hoặc `output_text`. Code phải xử lý cả hai.
- `max_output_tokens` là giới hạn độ dài output. Nếu output dài hơn, JSON sẽ bị cắt.

---

## Phần 5. JSON mode khác Structured Outputs thế nào

| | Structured Outputs | JSON mode |
|---|---|---|
| Output là JSON hợp lệ | Có | Có |
| Khớp schema bạn định nghĩa | Có | Không |
| Cách bật | `text.format` với `type: "json_schema"`, `strict: true` | `text.format` với `type: "json_object"` |

Trang docs khuyến nghị dùng Structured Outputs khi có thể. Với JSON mode:
- Prompt phải nói rõ model cần trả JSON. Nếu không, model có thể sinh vô hạn khoảng trắng cho đến khi chạm giới hạn token. API sẽ báo lỗi nếu chuỗi "JSON" không xuất hiện trong context.
- Bạn vẫn phải tự validate schema.

---

## Phần 6. Liên hệ với code W1 của bạn

`scripts/classify_one.py` đã dùng cách tương tự, nhưng theo Chat Completions API:

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
    response_format={
        "type": "json_schema",
        "json_schema": {"name": "issue_label", "strict": True, "schema": SCHEMA},
    },
)
```

Và sau đó validate bằng Pydantic:

```python
label = IssueLabel.model_validate_json(raw)
```

So với docs, W1 của bạn đã có:
- JSON schema với `strict: True`,
- validate bằng Pydantic,
- retry khi validate lỗi.

W2 cần thêm:
- kiểm tra `refusal` và `incomplete` (Phần 4),
- xử lý lỗi API: timeout, 429, 500 (theo guide W2),
- tách logic gọi model ra `app/services/llm.py`,
- đưa vào FastAPI endpoint `POST /analyze-meeting`.

---

## Phần 7. Câu tự kiểm tra

Trả lời được các câu này mà không nhìn tài liệu:

1. Structured Outputs khác JSON mode ở điểm nào? Vì sao docs khuyến nghị Structured Outputs?
2. Vì sao vẫn phải validate output phía server dù đã có schema?
3. Ba trường hợp nào khiến output không khớp schema? Cách phát hiện từng trường hợp?
4. Vì sao `root` của schema không được là `anyOf`?
5. Khi nào nên dùng function calling, khi nào nên dùng `text.format`?
6. Vì sao một prompt "hãy xin phép" không phải là cơ chế kiểm soát? (Câu này thuộc W6, nhưng nguyên tắc giống nhau: kiểm soát phải nằm trong code.)

---

## Ghi chú

- Đây là ghi chú học, không phải code của W2. Không chứa API key.
- Tên model trong ví dụ là tên docs. Khi làm W2, dùng model đã chốt trong `.env`.
