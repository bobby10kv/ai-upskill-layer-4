# Layer 4 — Agents & Orchestration (LangChain / DeepAgents)

This folder contains:

- Layer 4 session notes: `session-notes-layer-4.md`
- Reference notebook: `session-notes-layer-4.ipynb`
- Example scripts:
  - `scripts/langchain_agent.py` — LangChain `agent.invoke(...)` example
  - `scripts/deep_agent.py` — DeepAgents `deep_agent.invoke(...)` example
  - `scripts/agent.py` — small toy example showing tool wiring

## Setup

Create and activate a virtual environment (recommended), then install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in the repo root (it is gitignored) and set at least:

```bash
OPENAI_API_KEY="..."
```

Optional (for tracing/observability if you use LangSmith):

```bash
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY="..."
LANGSMITH_PROJECT="layer4-agents"
```

## Run examples

From the repo root (with `venv` activated):

```bash
python scripts/langchain_agent.py
python scripts/deep_agent.py
```

## Notes

- The “Gatsby” task intentionally highlights a key engineering point: **exact counts should be computed by deterministic tools**, not guessed by the model.

