# Hotel Concierge Agent

A mini AI agent built to prep for the Lingopal AI Agent Tech Lead role.

Handles the 3 most common hotel support requests, knows when it's out of its depth, and hands off to a human with full context. Built with FastAPI + Gemini tool use. No database, no auth, no infra — just working agent behavior.

---

## What it does

- **Reservation lookup** — find a guest's booking by name
- **Room upgrade requests** — approve or deny based on availability
- **Early check-in / late checkout** — approve or suggest alternatives
- **Escalation** — anything outside those 3 gets handed off immediately with full conversation context

---

## System Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Browser (Chrome)                  │
│                                                      │
│   🎙️ Web Speech API          ⌨️  Text Input          │
│          │                         │                 │
│          └──────────┬──────────────┘                 │
│                     │ user message                   │
└─────────────────────┼───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                 FastAPI Backend                      │
│                                                      │
│   POST /chat                POST /speak              │
│       │                         ▲                   │
│       ▼                         │                   │
│  Agent Loop                ElevenLabs TTS            │
│  concierge.py              voice.py                  │
│       │                         ▲                   │
│       ▼                         │ text response      │
│  Gemini (OpenAI-compatible) ────┘                   │
│       │                                              │
│       ├── lookup_reservation                         │
│       ├── request_upgrade                            │
│       ├── request_early_late_checkout                │
│       └── escalate_to_human                         │
│                   │                                  │
│            mock_pms.py                               │
│          (fake hotel data)                           │
└─────────────────────────────────────────────────────┘
                      │
                      ▼ audio stream
┌─────────────────────────────────────────────────────┐
│              Browser plays response                  │
└─────────────────────────────────────────────────────┘
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

Add your API keys to `.env`:

```
GEMINI_API_KEY=your_key_here        # free at aistudio.google.com
ELEVENLABS_API_KEY=your_key_here    # free tier at elevenlabs.io
```

---

## Run the voice UI

```bash
uvicorn app.main:app --reload
```

Open **http://localhost:8000** in Chrome. Click the mic and speak. The agent responds out loud via ElevenLabs. Use the text input if speech recognition mishears you. Hit "Reset conversation" to start a new scenario.

> Web Speech API only works in Chrome.

---

## Run the terminal test

```bash
python test_agent.py
```

Runs 3 scenarios without the UI. See `session1_output.txt` for actual output.

---

## Phases

### Phase 1 — Core Agent + Tools ✅
FastAPI skeleton, 3 mock PMS tools, Gemini tool loop, terminal test passing.

### Phase 2 — Escalation + Memory ✅
Escalation tool, conversation memory via message history, 3 test scenarios.

### Phase 3 — Voice Interface ✅
Web Speech API for STT, ElevenLabs for TTS, dark chat UI, typing fallback, reset button.

### Phase 4 — Polish + Demo Script ✅
Repo cleanup, `DEMO_SCRIPT.md` for recording the Loom.

---

## Stack

| Layer               | Choice                                   |
|---------------------|------------------------------------------|
| LLM + Tool Use      | Gemini (free tier via Google AI Studio)  |
| Agent Orchestration | Raw tool loop (OpenAI-compatible client) |
| Backend             | FastAPI                                  |
| Voice Input         | Web Speech API (Chrome)                  |
| Voice Output        | ElevenLabs TTS                           |
| Mock Data           | Hardcoded JSON, no DB needed             |

---

## What to Skip

- Auth, multi-tenancy, real database
- Multiple languages (Lingopal handles translation — keep scope tight)
- Deployment and infra

The goal is working agent behavior, not a production app.

---

## What This Demonstrates

- An agent that **acts**, not just chats
- Understanding of the hospitality/travel support vertical
- Clean escalation — the first thing every enterprise buyer asks about
- Shipping fast with tight scope

---

## Takeaway

The agent loop itself is simple — the hard part is the edge cases. Model returns `None`? Guard it. Free tier rate limits? Have a backup model. Tool logic wrong? Write a test that catches it before you demo.

The escalation path is the one thing you can't skip. It's the first question every enterprise buyer asks. Get that working cleanly and the rest is polish.
