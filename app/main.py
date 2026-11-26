import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.schemas import MeetingRequest, Summary
from app.scoring import check
from app.services.llm import analyze, judge_summary, LLMError

app = FastAPI(title="Delivery Assistant W2")

ROOT = Path(__file__).resolve().parent.parent
CASES_FILE = ROOT / "data/w2/meeting_cases.json"
DEMO_PAGE = Path(__file__).resolve().parent / "static/demo.html"

# Bảng map lỗi sang HTTP theo mục "Việc cần chốt" trong checklist
STATUS = {"timeout": 504, "rate_limit": 429, "upstream": 502, "bad_output": 502}


class CompareRequest(BaseModel):
    case_id: str
    predicted: Summary


class JudgeSummaryRequest(BaseModel):
    expected_summary: str
    predicted_summary: str


def load_cases():
    return json.loads(CASES_FILE.read_text(encoding="utf-8"))


@app.post("/analyze-meeting", response_model=Summary)
def analyze_meeting(req: MeetingRequest):
    try:
        return analyze(req.meeting_text)
    except LLMError as e:
        raise HTTPException(status_code=STATUS[e.kind], detail=e.kind)


@app.get("/demo", response_class=HTMLResponse)
def demo_page():
    return DEMO_PAGE.read_text(encoding="utf-8")


@app.get("/demo-api/cases")
def demo_cases():
    cases = load_cases()
    return [{"id": c["id"], "title": c["title"], "group": c["group"], "input": c["input"]} for c in cases]


@app.post("/demo-api/compare")
def demo_compare(req: CompareRequest):
    case = next((c for c in load_cases() if c["id"] == req.case_id), None)
    if case is None:
        raise HTTPException(status_code=404, detail="case_not_found")
    got = req.predicted.model_dump()
    reason = check(case["expected"], got)
    return {
        "pass": reason == "",
        "reason": reason,
        "expected": case["expected"],
    }


@app.post("/demo-api/judge-summary")
def demo_judge_summary(req: JudgeSummaryRequest):
    # Chỉ so nghĩa summary; không đổi PASS/FAIL từ check()
    try:
        result = judge_summary(req.expected_summary, req.predicted_summary)
    except LLMError as e:
        raise HTTPException(status_code=STATUS[e.kind], detail=e.kind)
    return {
        "same_meaning": result["same_meaning"],
        "expected_summary": req.expected_summary,
        "predicted_summary": req.predicted_summary,
    }
