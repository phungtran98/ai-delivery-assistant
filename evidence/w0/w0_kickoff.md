# W0 Kickoff – Commands and Results

**Environment:** Linux, Python 3.13.0 (pyenv), Git, venv in `.venv/`.

## Commands run (in order)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set OPENAI_API_KEY, OPENAI_BASE_URL=https://api.groq.com/openai/v1, OPENAI_MODEL=openai/gpt-oss-120b
python scripts/smoke_test.py
pytest -q tests/test_mock_jira.py
uvicorn app.mock_jira:app --port 8001
curl -H 'X-Allowed-Project: ALPHA' http://127.0.0.1:8001/projects/ALPHA/sprints/12/issues
```

## Results

- `pip check`: no broken requirements.
- `scripts/smoke_test.py`: `PASS - fixture files and counts are consistent` (documents 15, jira_issues 30, issue_cases 20, retrieval_cases 20, rag_cases 30, agent_cases 20, security_cases 10).
- `pytest -q tests/test_mock_jira.py`: `3 passed` (one Starlette deprecation warning about `httpx` in `TestClient`).
- `GET /docs` on port 8001: `200 OK`.
- `curl` with `X-Allowed-Project: ALPHA` on sprint 12: 10 issues, `ALPHA-101` to `ALPHA-110`.

## Notes

- `.env` and `.venv/` are listed in `.gitignore` and are not committed.
- API keys are not recorded in this file.
