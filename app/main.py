from fastapi import FastAPI, HTTPException
from app.schemas import MeetingRequest, Summary
from app.services.llm import analyze, LLMError

app = FastAPI(title="Delivery Assistant W2")

# Bảng map lỗi sang HTTP theo mục "Việc cần chốt" trong checklist
STATUS = {"timeout": 504, "rate_limit": 429, "upstream": 502, "bad_output": 502}


@app.post("/analyze-meeting", response_model=Summary)
def analyze_meeting(req: MeetingRequest):
    try:
        return analyze(req.meeting_text)
    except LLMError as e:
        raise HTTPException(status_code=STATUS[e.kind], detail=e.kind)
