# Bài 2 — OpenAI Structured Outputs

**Ngày học:** 24/11/2026  
**Mục tiêu:** Hiểu khái niệm, thực hành Python, phân biệt JSON Mode với Structured Outputs và biết các lưu ý khi tích hợp API.

## 1. Structured Outputs là gì?

Structured Outputs (đầu ra có cấu trúc) giúp AI trả về dữ liệu tuân theo JSON Schema đã định nghĩa, khi phản hồi hoàn tất thành công và không bị từ chối. Nhờ vậy, chương trình có thể lấy từng trường dữ liệu để xử lý thay vì phải tự tách nội dung từ một đoạn văn bản.

**Câu đã chốt:** Structured Outputs là tính năng giúp AI trả về dữ liệu đúng cấu trúc Schema mà mình đã định nghĩa.

Ví dụ input: `Nguyễn Văn An, 22 tuổi, là lập trình viên.`

Đầu ra thông thường: Nguyễn Văn An là một lập trình viên 22 tuổi.

Đầu ra có cấu trúc:

```json
{
  "name": "Nguyễn Văn An",
  "age": 22,
  "job": "Lập trình viên"
}
```

Ứng dụng: trích xuất thông tin, lưu database, điền biểu mẫu, tích hợp backend và giao diện.

## 2. Schema, JSON Schema và Pydantic

- **Schema:** Bản mô tả cấu trúc dữ liệu, gồm tên trường, kiểu dữ liệu và các ràng buộc.
- **JSON Schema:** Cách biểu diễn các quy tắc đó bằng JSON.
- **Pydantic:** Thư viện Python dùng để khai báo, kiểm tra và chuyển đổi dữ liệu theo mô hình.
- **BaseModel:** Lớp cơ sở của Pydantic mà mình kế thừa để khai báo mô hình dữ liệu.

**Cách nhớ đã chốt:** Schema giống như một cái form có các ô và quy tắc phải tuân theo. Trong bài này, AI là bên tạo dữ liệu theo form đó; không nhất thiết người dùng phải tự điền.

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    job: str
```

JSON Schema tương ứng về mặt ý nghĩa (minh họa rút gọn theo yêu cầu strict):

```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "job": {"type": "string"}
  },
  "required": ["name", "age", "job"],
  "additionalProperties": false
}
```

## 3. Thực hành Python — Responses API

Cài thư viện trong đúng môi trường Python đang chạy:

```bash
python -m pip install -U openai pydantic
```

Đặt biến môi trường `OPENAI_API_KEY` trước khi chạy. Không ghi API key trực tiếp vào code hoặc đưa lên Git.

Tạo file `structured_outputs.py`:

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class Person(BaseModel):
    name: str
    age: int
    job: str

response = client.responses.parse(
    model="gpt-6.2-astra",
    instructions="Trích xuất thông tin cá nhân.",
    input="Nguyễn Văn An, 22 tuổi, là lập trình viên.",
    text_format=Person
)

person = response.output_parsed

if person is not None:
    print("Name:", person.name)
    print("Age:", person.age)
    print("Job:", person.job)
else:
    print("Không nhận được dữ liệu.")
```

**Ghi chú model:** Trong buổi học mình dùng `gpt-6-luna` và bạn báo đã chạy ra kết quả. Ví dụ trên dùng `gpt-6.2-astra`, ID trong ví dụ Python của tài liệu chính thức được đối chiếu khi tổng kết. Bạn có thể giữ model đã chạy được trong tài khoản của mình nếu model đó hỗ trợ Structured Outputs. Không cần đổi chỉ vì tên model trong ví dụ khác.

Kết quả mong đợi:

```text
Name: Nguyễn Văn An
Age: 22
Job: Lập trình viên
```

Bạn đã báo chạy thành công và nhận được ba trường riêng biệt trong buổi thực hành. Code trong file tổng kết không được gọi API chạy lại.

## 4. Các tham số, phương thức và thuộc tính đã học

| Thuật ngữ | Vai trò |
| --- | --- |
| `model` | Chọn model AI. |
| `instructions` | Chỉ dẫn AI làm nhiệm vụ gì và theo quy tắc nào. |
| `input` | Dữ liệu hoặc yêu cầu gửi cho AI. |
| `text_format=Person` | Gắn mô hình dữ liệu Person vào lời gọi SDK để quy định đầu ra. |
| `client.responses.parse()` | Gửi request và hỗ trợ phân tích kết quả thành đối tượng Pydantic. |
| `response.output_parsed` | Lấy đối tượng dữ liệu đã được phân tích (hoặc None nếu không có). |
| `response.output_text` | Lấy nội dung văn bản đầu ra, khác với đối tượng đã parse. |

**Các câu đã chốt:**

- BaseModel là cái khung để khai báo dữ liệu.
- Schema định nghĩa cấu trúc; `text_format` gắn cấu trúc đó vào lời gọi API.
- `parse()` gửi yêu cầu và hỗ trợ phân tích kết quả; `output_parsed` chứa kết quả đã phân tích.

**Lưu ý:** Việc parse thành đối tượng Python là công việc của SDK, không phải AI trực tiếp tạo đối tượng Python trên máy mình. `text_format` là tham số tiện ích của Python SDK; cấu hình JSON Schema ở tầng Responses API nằm trong `text.format`.

Luồng xử lý:

```text
Input + Instructions + Schema
           ↓
        AI model
           ↓
   Đầu ra JSON theo Schema
           ↓
    SDK parse kết quả
           ↓
   response.output_parsed
           ↓
  person.name / age / job
```

## 5. JSON Mode và Structured Outputs

| Tiêu chí | JSON Mode | Structured Outputs |
| --- | --- | --- |
| JSON hợp lệ | Có, trong trường hợp thành công thông thường | Có |
| Đúng Schema đã định nghĩa | Không đảm bảo | Có, với schema được hỗ trợ và phản hồi thành công |
| Ví dụ tuổi | Có thể là `"22"` hoặc `22` | Phải là số nguyên nếu khai báo integer |
| Khi nên dùng | Khi chỉ cần JSON hoặc không có hỗ trợ schema | Khi ứng dụng cần cấu trúc dữ liệu nhất quán |

**Câu đã chốt:** JSON Mode chỉ cần trả về JSON hợp lệ. Structured Outputs trả về JSON và JSON đó phải đúng Schema mình đã định nghĩa.

## 6. Liên hệ với Function Calling

Cả hai đều có thể sử dụng JSON Schema, nhưng mục đích khác nhau.

| Function Calling (strict) | Structured Outputs cho câu trả lời |
| --- | --- |
| Quy định đối số AI truyền vào hàm | Quy định cấu trúc dữ liệu AI trả về cho mình |
| `parameters` và `strict=True` | `text_format=Person` với Python SDK |
| Ví dụ: `get_price(product="laptop")` | Ví dụ: `{"name": "An", "age": 22, "job": "IT"}` |

**Câu bạn đã diễn giải đúng:** Trong Function Calling, Schema quyết định cấu trúc đối số mà AI truyền vào hàm của mình. Còn Structured Outputs thông qua `text_format`, Schema quyết định cấu trúc mà AI trả về cho mình.

Nhớ bài trước: AI yêu cầu gọi hàm, Python thực thi hàm. Function Calling không tự đảm bảo câu trả lời cuối cùng có cấu trúc nếu mình không cấu hình thêm.

## 7. Giới hạn và lưu ý

**Rule quan trọng nhất đã chốt:** Structured Outputs đảm bảo cấu trúc, chứ không đảm bảo tất cả thông tin đều đúng thực tế.

Ví dụ: `age: 99` vẫn đúng kiểu integer, nhưng có thể sai so với dữ liệu gốc là 22 tuổi. Do đó cần kiểm tra nghiệp vụ và nguồn dữ liệu. Nếu input thiếu thông tin, nên cho phép giá trị null khi thích hợp và chỉ dẫn AI không bịa thông tin. Không phải mọi tính năng của JSON Schema đều được hỗ trợ.

## 8. Edge Cases — Các trường hợp đặc biệt

| Trường hợp | Ý nghĩa | Cách xử lý |
| --- | --- | --- |
| Refusal | AI từ chối yêu cầu | Kiểm tra nội dung refusal và thông báo phù hợp. |
| Incomplete Response | Phản hồi chưa hoàn tất, ví dụ chạm giới hạn token | Kiểm tra status, incomplete_details; không sử dụng dữ liệu dang dở. |
| API Error | Lỗi khi gọi API, ví dụ lỗi kết nối, quyền truy cập hoặc request sai | Bắt lỗi, đọc thông báo và sửa nguyên nhân. |

**Câu đã chốt:** Không nên mặc định AI luôn trả về dữ liệu thành công, vì AI có thể từ chối, trả lời dang dở hoặc có lỗi API.

`if person is not None` là bước kiểm tra cơ bản. Khi triển khai thật, cần kiểm tra thêm `response.status`, nội dung refusal và bắt ngoại lệ. SDK cũng có thể ném lỗi ngay trong quá trình parse nếu dữ liệu không đầy đủ hoặc không hợp lệ.

## 9. Lưu ý thực hành trong buổi học

- Dòng import chính xác: `from pydantic import BaseModel`. Tên `pydantic` viết thường; `BaseModel` viết liền, B và M viết hoa.
- Nếu chưa cài Pydantic, dùng `python -m pip install pydantic` và kiểm tra Python Interpreter của VS Code.
- Không cần `import json` trong ví dụ dùng `responses.parse()`; khác với ví dụ Function Calling thủ công có `json.loads()`.
- Trong lúc thực hành có gặp lỗi và sau đó bạn tự kiểm tra, chạy thành công. Không có nội dung lỗi đầy đủ nên không kết luận nguyên nhân cụ thể.
- Nếu gặp `BadRequestError` (HTTP 400), đọc trường `message` để tìm nguyên nhân; không tự mặc định là lỗi import.

## 10. Thuật ngữ tiếng Anh và cách phát âm

Cách đọc tiếng Việt chỉ là gợi ý gần đúng; chữ in hoa chỉ âm nhấn.

| Từ | IPA (tham khảo Anh-Mỹ) | Cách đọc gần đúng |
| --- | --- | --- |
| Structured Outputs | /ˈstrʌktʃərd ˈaʊtpʊts/ | STRẮC-chờrd AO-pụts |
| Schema | /ˈskiːmə/ | SKII-mờ |
| Pydantic | /paɪˈdæntɪk/ | pai-ĐEN-tik |
| BaseModel | /beɪs ˈmɑːdəl/ | bêys MO-đồ |
| Parse | /pɑːrs/ | pars |
| Parsed | /pɑːrst/ | parst |
| JSON Mode | /ˈdʒeɪsən moʊd/ | JÂY-sần môud |
| Edge Cases | /edʒ ˈkeɪsɪz/ | ej KÂY-siz |
| Refusal | /rɪˈfjuːzəl/ | ri-FIU-zồ |
| Incomplete Response | /ˌɪnkəmˈpliːt rɪˈspɑːns/ | in-cầm-PLIIT ri-SPONS |
| API Error | /ˌeɪ piː ˈaɪ ˈerər/ | ây-pi-ai E-rờ |

Tên chính xác là **Structured Outputs** (có âm cuối ở cả hai từ). `output_parsed` đọc theo thứ tự output underscore parsed, không phải parse underscore output.

## 11. Ôn nhanh trước khi trình bày với sếp

1. Structured Outputs là gì? — Tính năng quy định cấu trúc dữ liệu đầu ra của AI.
2. Schema là gì? — Bản mô tả trường, kiểu dữ liệu và các quy tắc.
3. BaseModel dùng làm gì? — Lớp cơ sở để khai báo mô hình dữ liệu Pydantic.
4. text_format dùng làm gì? — Gắn mô hình dữ liệu vào lời gọi SDK.
5. parse và output_parsed khác gì? — Một phương thức xử lý lời gọi và phân tích kết quả; một thuộc tính lấy kết quả đã phân tích.
6. JSON Mode khác Structured Outputs thế nào? — JSON hợp lệ khác với JSON vừa hợp lệ vừa đúng Schema.
7. Function Calling khác ở đâu? — Schema của function tool ràng buộc đối số gọi hàm, không phải câu trả lời cuối.
8. Structured Outputs đảm bảo nội dung đúng thực tế không? — Không, cần xác thực dữ liệu.
9. Ba trường hợp đặc biệt cần xử lý? — Refusal, Incomplete Response, API Error.

### Đoạn trình bày ngắn

Structured Outputs là tính năng của OpenAI giúp AI trả về dữ liệu đúng Schema mình định nghĩa. Trong Python, mình có thể dùng Pydantic để khai báo Schema, truyền qua text_format, gọi responses.parse và lấy đối tượng từ output_parsed. Khác với JSON Mode, Structured Outputs ràng buộc cả cấu trúc dữ liệu, không chỉ định dạng JSON. Tuy nhiên, đúng cấu trúc không đồng nghĩa đúng sự thật, và mình cần xử lý các trường hợp từ chối, phản hồi chưa hoàn thành hoặc lỗi API.

## 12. Tài liệu tham khảo

- [OpenAI — Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) (đối chiếu ngày 24/11/2026).
- [OpenAI — Function Calling](https://developers.openai.com/api/docs/guides/function-calling).
- [Pydantic — Documentation](https://docs.pydantic.dev/).

---
**Quy tắc học đã thống nhất:** Hiểu khái niệm → thực hành code → tự diễn giải → chỉnh thuật ngữ và phát âm → chốt kiến thức → tổng kết Markdown cuối buổi.
