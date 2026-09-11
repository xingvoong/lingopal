# Hotel Concierge Agent

A mini AI agent project built to prep for the Lingopal AI Agent Tech Lead role.

The agent handles the 3 most common hotel support requests, knows when it's out of its depth, and hands off to a human with full context. Built with FastAPI + Gemini tool use. No database, no auth, no infra — just working agent behavior.

---

## What it does

- **Reservation lookup** — find a guest's booking by name
- **Room upgrade requests** — approve or deny based on availability
- **Early check-in / late checkout** — approve or suggest alternatives
- **Escalation** — anything outside those 3 (complaints, refunds, billing) gets handed off to a human agent immediately, with the full conversation context

---

## How it works

```
User message
     │
     ▼
Agent loop (concierge.py)
     │
     ▼
Gemini 3.6 Flash ──► calls one of 4 tools
     │
     ├── lookup_reservation
     ├── request_upgrade
     ├── request_early_late_checkout
     └── escalate_to_human
              │
              ▼
       mock_pms.py (fake hotel data)
              │
              ▼
       result injected back into history
              │
              ▼
       model generates final response
```

---

## Setup

```bash
git clone https://github.com/xingvoong/lingopal.git
cd lingopal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your Gemini API key (free at [aistudio.google.com](https://aistudio.google.com)):

```
echo "GEMINI_API_KEY=your_key_here" > .env
```

---

## Run the terminal test

```bash
python test_agent.py
```

Runs 3 scenarios: reservation lookup + upgrade, late checkout request, and a complaint that triggers escalation. See `session1_output.txt` for actual output.

---

## Run the API

```bash
uvicorn app.main:app --reload
```

POST to `/chat`:

```json
{
  "message": "Hi, I'd like to look up my reservation. My name is Alice Chen.",
  "history": []
}
```

Returns:

```json
{
  "response": "Hello Alice! I found your reservation...",
  "history": [...]
}
```

Pass `history` from the previous response to maintain conversation context across turns.

---

## What's next

- Phase 3: Chat UI (Next.js or plain HTML + SSE for streaming)
- Phase 4: Loom demo + polish

---

## Stack

| Layer | Choice |
|---|---|
| LLM | Gemini 3.6 Flash (free tier) |
| API client | OpenAI-compatible SDK |
| Backend | FastAPI |
| Mock data | Hardcoded Python dicts |
