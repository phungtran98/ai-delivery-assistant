import json
import os
from openai import OpenAI, APITimeoutError, RateLimitError
from pydantic import ValidationError
from app.schemas import Summary


class LLMError(Exception):
    # kind: "timeout", "rate_limit", "upstream" hoặc "bad_output"
    def __init__(self, kind):
        super().__init__(kind)
        self.kind = kind


def strict_schema(node):
    # OpenAI strict yêu cầu: mỗi object không có thuộc tính thừa, và liệt kê đủ mọi thuộc tính
    if isinstance(node, dict):
        if node.get("type") == "object":
            node["additionalProperties"] = False
            node["required"] = list(node["properties"].keys())
        for value in node.values():
            strict_schema(value)
    elif isinstance(node, list):
        for item in node:
            strict_schema(item)
    return node


SCHEMA = strict_schema(Summary.model_json_schema())

PROMPT = """Extract the summary, decisions, and action items from the meeting notes.
- Use only information in the meeting notes. Do not guess.
- If the owner is not clear, set owner = null. Do not take the owner from the attendee list.
- If the date is not clear, set due_date = null.
- Relative dates (for example "next Friday") set due_date = null.
- Dates without a year use the year of the meeting date.
- Absolute dates (for example "November 25, 2026") use the format YYYY-MM-DD.
- A decision is something the team explicitly agreed on, including agreements like "needs improvement" or "is necessary", even if no owner or task was assigned yet.
- Do not create a decision from the absence of a decision (for example, "no decision was made"), from a postponed decision, or from a mere proposal/suggestion.
- A suggestion is not an action unless a person explicitly accepts it.
- Speculation or vague statements are not actions.
- If a task is assigned to two or more people, create one action per person.
- Each separate decision is one item. Do not merge decisions.
- When the team moves a deadline, record one decision for the new deadline. Do not add a separate decision that the old deadline is no longer valid.
- Keep the overall milestone deadline distinct from each person's task due_date.
- Write summary, decisions, and actions in English.

Meeting notes:
"""


def analyze(text):
    # Đọc biến môi trường trước khi gọi API, để thiếu biến thì báo lỗi rõ ràng
    api_key = os.environ["OPENAI_API_KEY"]
    base_url = os.environ["OPENAI_BASE_URL"]
    model = os.environ["W2_MODEL"]

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=30.0,   # đợi tối đa 30 giây
        max_retries=0,  # tự kiểm soát retry, không để SDK retry ngầm
    )

    # Thử tối đa 2 lần nếu JSON trả về sai khuôn
    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": PROMPT + text}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {"name": "meeting_summary", "strict": True, "schema": SCHEMA},
                },
            )
        except APITimeoutError:
            raise LLMError("timeout")
        except RateLimitError:
            raise LLMError("rate_limit")
        except Exception:
            raise LLMError("upstream")

        try:
            return Summary.model_validate_json(response.choices[0].message.content)
        except ValidationError:
            pass  # sai khuôn, thử lại

    raise LLMError("bad_output")


JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"same_meaning": {"type": "boolean"}},
    "required": ["same_meaning"],
    "additionalProperties": False,
}


def judge_summary(expected, predicted):
    # So sánh nghĩa summary Gold vs AI; không ảnh hưởng Gate check()
    api_key = os.environ["OPENAI_API_KEY"]
    base_url = os.environ["OPENAI_BASE_URL"]
    model = os.environ["W2_MODEL"]

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=30.0,
        max_retries=0,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": (
                f"Expected summary: {expected}\n"
                f"Predicted summary: {predicted}\n"
                "Does the predicted summary state the same main points as the expected summary? Answer in JSON."
            )}],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "summary_judge", "strict": True, "schema": JUDGE_SCHEMA},
            },
        )
    except APITimeoutError:
        raise LLMError("timeout")
    except RateLimitError:
        raise LLMError("rate_limit")
    except Exception:
        raise LLMError("upstream")

    try:
        data = json.loads(response.choices[0].message.content or "")
        same = data["same_meaning"]
    except (json.JSONDecodeError, KeyError, TypeError):
        raise LLMError("bad_output")
    if not isinstance(same, bool):
        raise LLMError("bad_output")
    return {"same_meaning": same}
