# Hotel Concierge Agent — Project Plan

A mini AI agent project to prep for the Lingopal AI Agent Tech Lead role.
Scope: 2 weekends. One working demo with real agent behavior.

---

## System Diagram

```
User (Chat or Voice)
        │
        ▼
┌───────────────────┐
│   Interface Layer  │
│  (FastAPI + UI or  │
│   Voice via        │
│   Whisper + TTS)   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   Agent Loop       │
│  (Claude + Tool    │
│   Use / LangGraph) │
└────────┬──────────┘
         │
    ┌────┴─────┐
    │  Tools   │
    └────┬─────┘
         │
  ┌──────┼──────────┐
  ▼      ▼          ▼
lookup  request   escalate
 res.   upgrade   to human
  │      │          │
  └──────┴──────────┘
         │
         ▼
  Mock Hotel PMS
  (fake JSON data)
         │
         ▼
  Escalation Path
  (full context handoff)
```

---

## Phases

### Phase 1 — Weekend 1, Day 1: Core Agent + Tools

**Goal:** Agent loop running locally with all 3 tools wired up.

- Set up FastAPI project skeleton
- Define 3 mock tools:
  - `lookup_reservation(guest_name, dates)` — returns fake booking JSON
  - `request_upgrade(reservation_id, room_type)` — returns approval/denial
  - `request_early_late_checkout(reservation_id, time)` — returns availability
- Wire tools into Claude API tool use (or LangGraph node graph)
- Test the agent loop in the terminal — no UI yet

**Done when:** You can type a request and the agent calls the right tool and returns a coherent response.

---

### Phase 2 — Weekend 1, Day 2: Escalation + Memory

**Goal:** Agent knows when to quit and hands off cleanly.

- Add escalation tool: `escalate_to_human(reason, conversation_history)`
- Define clear escalation triggers (e.g. complaints, refunds, edge cases the agent can't handle)
- Add short-term conversation memory so context carries across turns
- Write 5 test scenarios that cover the happy path and the escalation path

**Done when:** The agent handles the 3 core requests and escalates everything else with full context.

---

### Phase 3 — Weekend 2, Day 1: Interface

**Goal:** A real interface, not just a terminal.

- Option A (faster): Simple chat UI with Next.js or plain HTML + JS, SSE for streaming
- Option B (higher signal): Voice interface — Whisper for STT, ElevenLabs or pyttsx3 for TTS

Pick one. Don't do both. Voice is higher signal for this role.

**Done when:** You can demo it to someone over a screen share without explaining the terminal.

---

### Phase 4 — Weekend 2, Day 2: Polish + Demo Script

**Goal:** A demo you'd actually show in an interview.

- Record a 2-minute Loom demo covering:
  1. A successful reservation lookup
  2. An upgrade request (approval and denial)
  3. An escalation with context handoff
- Write a short README: what it does, how to run it, what you'd build next
- Clean up the repo — no dead code, no TODO comments left in

**Done when:** You'd send the GitHub link without hesitation.

---

## Stack

| Layer              | Choice                        |
|--------------------|-------------------------------|
| LLM + Tool Use     | Claude API (Anthropic)        |
| Agent Orchestration| LangGraph or raw tool loop    |
| Backend            | FastAPI                       |
| Voice (optional)   | Whisper (STT) + ElevenLabs (TTS) |
| Mock Data          | Hardcoded JSON, no DB needed  |
| Hosting            | Run locally for the demo      |

---

## What to Skip

- Auth, multi-tenancy, real database
- Multiple languages (even though Lingopal does translation — keep scope tight)
- Deployment and infra

The goal is working agent behavior, not a production app.

---

## What This Demonstrates

- You can build an agent that **acts**, not just chats
- You understand the hospitality/travel support vertical
- You know how to handle the escalation problem — the thing every enterprise buyer asks about first
- You ship fast and keep scope tight
