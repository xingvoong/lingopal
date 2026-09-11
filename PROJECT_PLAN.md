# Hotel Concierge Agent — Project Plan

A mini AI agent project to prep for the Lingopal AI Agent Tech Lead role.
One working voice demo with real agent behavior.

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

## Phases

### Phase 1 — Core Agent + Tools ✅

**Goal:** Agent loop running locally with all 3 tools wired up.

- Set up FastAPI project skeleton
- Define 3 mock tools:
  - `lookup_reservation(guest_name)` — returns fake booking JSON
  - `request_upgrade(reservation_id, room_type)` — returns approval/denial
  - `request_early_late_checkout(reservation_id, type, time)` — returns availability
- Wire tools into Gemini via OpenAI-compatible client
- Test the agent loop in the terminal — no UI yet

**Result:** All 3 tools working. Agent calls the right tool and returns a coherent response. See `session1_output.txt`.

---

### Phase 2 — Escalation + Memory ✅

**Goal:** Agent knows when to quit and hands off cleanly.

- Add escalation tool: `escalate_to_human(reason, summary)`
- Clear escalation triggers: complaints, refunds, billing disputes
- Conversation memory via message history passed each turn
- 3 test scenarios covering happy path and escalation

**Result:** Escalation working cleanly. Complaint → immediate handoff with full context.

---

### Phase 3 — Voice Interface ✅

**Goal:** A real interface, not just a terminal.

- Browser mic via Web Speech API — no Whisper install needed
- ElevenLabs TTS — natural voice responses via `/speak` endpoint
- Dark chat UI served from FastAPI at `http://localhost:8000`
- Typing fallback with Enter-to-send
- Escalation detection highlights handoff bubbles in amber
- Reset button to clear history and start a new scenario

**Result:** Full voice loop working in Chrome — speak, agent thinks, ElevenLabs responds out loud.

---

### Phase 4 — Polish + Demo Script ✅

**Goal:** A demo you'd actually show in an interview.

- Fixed broken `.gitignore`
- No TODO comments or dead code
- Wrote `DEMO_SCRIPT.md` — exact words to say, setup steps, recording tips

**Next:** Record the Loom following `DEMO_SCRIPT.md`. Escalation scenario last — strongest ending.

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

- You can build an agent that **acts**, not just chats
- You understand the hospitality/travel support vertical
- You know how to handle the escalation problem — the thing every enterprise buyer asks about first
- You ship fast and keep scope tight

---

## Takeaway

The agent loop itself is simple — the hard part is the edge cases. Model returns `None`? Guard it. Free tier rate limits? Have a backup model. Tool logic wrong? Write a test that catches it before you demo.

The escalation path is the one thing you can't skip. It's the first question every enterprise buyer asks. Get that working cleanly and the rest is polish.
