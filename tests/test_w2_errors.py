import json
from types import SimpleNamespace

import httpx
from fastapi.testclient import TestClient
from openai import APIStatusError, APITimeoutError, RateLimitError

from app import main
from app.schemas import Summary
from app.services import llm

REQ = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
TEXT = "Biên bản họp đủ dài để qua kiểm tra 20 ký tự."
VALID = json.dumps({
    "summary": "Nhóm thống nhất ưu tiên lỗi đăng nhập.",
    "decisions": ["Ưu tiên lỗi đăng nhập."],
    "actions": [{"owner": None, "action": "Rà soát PR.", "due_date": None}],
})


def ok(content):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


def fake_model(monkeypatch, behavior):
    # behavior là hàm không tham số, trả response hoặc raise lỗi
    calls = {"n": 0}

    class FakeCompletions:
        def create(self, **kwargs):
            calls["n"] += 1
            return behavior()

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(llm, "OpenAI", FakeOpenAI)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "http://fake")
    monkeypatch.setenv("W2_MODEL", "fake-model")
    return calls


def post(text=TEXT):
    return TestClient(main.app).post("/analyze-meeting", json={"meeting_text": text})


def test_bad_input_422_no_model_call(monkeypatch):
    calls = fake_model(monkeypatch, lambda: ok(VALID))
    assert post("   ").status_code == 422
    assert calls["n"] == 0


def test_timeout_504(monkeypatch):
    def boom():
        raise APITimeoutError(request=REQ)
    fake_model(monkeypatch, boom)
    r = post()
    assert r.status_code == 504 and r.json()["detail"] == "timeout"


def test_rate_limit_429(monkeypatch):
    def boom():
        raise RateLimitError("limit", response=httpx.Response(429, request=REQ), body=None)
    fake_model(monkeypatch, boom)
    r = post()
    assert r.status_code == 429 and r.json()["detail"] == "rate_limit"


def test_upstream_500_502(monkeypatch):
    def boom():
        raise APIStatusError("server error", response=httpx.Response(500, request=REQ), body=None)
    fake_model(monkeypatch, boom)
    r = post()
    assert r.status_code == 502 and r.json()["detail"] == "upstream"


def test_bad_json_retry_then_502(monkeypatch):
    calls = fake_model(monkeypatch, lambda: ok("không phải JSON"))
    r = post()
    assert calls["n"] == 2
    assert r.status_code == 502 and r.json()["detail"] == "bad_output"


def test_success_matches_schema(monkeypatch):
    fake_model(monkeypatch, lambda: ok(VALID))
    r = post()
    assert r.status_code == 200
    Summary.model_validate(r.json())
