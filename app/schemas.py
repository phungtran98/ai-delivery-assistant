from typing import Annotated
from pydantic import BaseModel, StringConstraints

NonBlank = Annotated[str, StringConstraints(strip_whitespace=True, min_length=20)]

class MeetingRequest(BaseModel):
    meeting_text: NonBlank  # biên bản họp; chuỗi trắng hoặc dưới 20 ký tự → 422

class ActionItem(BaseModel):
    owner: str | None  # không rõ thì None, không đoán
    action: str
    due_date: str | None  # YYYY-MM-DD hoặc null (ngày tương đối / không rõ → null)

class Summary(BaseModel):
    summary: str
    decisions: list[str]
    actions: list[ActionItem]
