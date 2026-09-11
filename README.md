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
Browser mic (Web Speech API)
     │  speech-to-text in Chrome
     ▼
FastAPI /chat
     │
     ▼
Gemini (OpenAI-compatible) ──► calls one of 4 tools
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
       text response back to browser
              │
              ▼
FastAPI /speak ──► ElevenLabs TTS
     │
     ▼
Audio plays in browser
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

## What's next

- Phase 4: Loom demo + final polish

---

## Stack

| Layer | Choice |
|---|---|
| LLM | Gemini (free tier via Google AI Studio) |
| API client | OpenAI-compatible SDK |
| Backend | FastAPI |
| Voice input | Web Speech API (Chrome) |
| Voice output | ElevenLabs TTS |
| Mock data | Hardcoded Python dicts |
