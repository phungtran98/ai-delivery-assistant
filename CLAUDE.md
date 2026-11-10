# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

This is the member starter kit for an 8-week "AI Engineering Fast-Track" training program (v12). Members build an **AI-Powered Delivery Assistant** (RAG Q&A over project docs, sprint health analysis via a read-only Jira mock, weekly status drafts, PM review/permissions). The kit ships only synthetic fixtures, a mock Jira API, and scoring scripts — **not** completed solutions. The parent directory has `AI_Engineering_Fast_Track_Summary.md` (Vietnamese summary of the program: features F01–F04, reference architecture, scoring gates). The slide deck is authoritative for requirements; `assignments/W0N_START_HERE.md` are short handoff stubs.

Target architecture for member work: FastAPI backend → agent service (tool orchestration) → RAG (docs → chunks → embeddings → Postgres/pgvector) + mock Jira REST + OpenAI API → PM review/approval.

## Commands

Run from this directory (Python 3.11+, venv):

```
pip install -r requirements.txt
python scripts/smoke_test.py                      # validates fixture counts; must end with PASS
pytest -q tests/test_mock_jira.py                 # expects 3 passed
pytest -q tests/test_mock_jira.py::<test_name>    # single test
uvicorn app.mock_jira:app --reload --port 8001    # docs at /docs
docker compose up -d db                           # pgvector (pg16) on 127.0.0.1:5432, for W3+
python scripts/evaluate_issue_classifier.py evidence/w1_predictions.csv
```

CSV header for the classifier scorer: `issue_id,predicted_category,predicted_priority`. `.env.example` lists `OPENAI_API_KEY`, `OPENAI_MODEL`, `DATABASE_URL`; copy to `.env` (never commit). There is no linter or build config. `pytest.ini` sets `pythonpath = .` so tests import `app.*`.

## Architecture notes

- `app/mock_jira.py` is the only application code: a read-only FastAPI app loading `data/jira/issues.json` at import. Endpoints: `/projects/{key}`, `/projects/{key}/sprints/{sprint_id}/issues`, `/issues/{issue_key}`. Authorization is the `X-Allowed-Project` header which must equal the project being accessed (403 otherwise, 404 for unknown project/issue). This is a teaching mock, explicitly not production auth — W7 replaces it with real authN/authZ. For `/issues/{key}` the 404-vs-403 order matters for cross-project leak tests.
- `data/documents/` — 15 synthetic docs (REQ/TEC/PM × 5, `.md`/`.txt`) plus `manifest.json`; the RAG corpus.
- `data/evaluation/` — gold sets (issue classification, retrieval, RAG, agent, security cases). `scripts/smoke_test.py` asserts exact counts (15 docs, 30 issues, 20/20/30/20/10 cases), so editing fixtures requires updating it. Do not modify gold labels; hidden mentor fixtures must stay out of this kit.
- `evidence/weekly_pr_template.md` — required PR/evidence structure for weekly submissions.

## Conventions

- Existing code is terse/compact style (minimal whitespace); match it when editing `app/` and `scripts/`.
- Synthetic data only: no real customer data to model APIs, and no Jira writes (mock is read-only by design).
- Requirements call for grounded, cited answers, refusing when info is missing, and zero cross-project leaks.
