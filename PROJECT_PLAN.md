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

### Phase 1 — Weekend 1, Day 1: Core Agent + Tools ✅

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

### Phase 2 — Weekend 1, Day 2: Escalation + Memory ✅

**Goal:** Agent knows when to quit and hands off cleanly.

- Add escalation tool: `escalate_to_human(reason, summary)`
- Clear escalation triggers: complaints, refunds, billing disputes
- Conversation memory via message history passed each turn
- 3 test scenarios covering happy path and escalation

**Result:** Escalation working cleanly. Complaint → immediate handoff with full context.

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

| Layer              | Choice                                      | Status    |
|--------------------|---------------------------------------------|-----------|
| LLM + Tool Use     | Gemini 3.6 Flash (via Google AI Studio)     | Done      |
| Agent Orchestration| Raw tool loop (OpenAI-compatible client)    | Done      |
| Backend            | FastAPI                                     | Done      |
| Mock Data          | Hardcoded JSON, no DB needed                | Done      |
| Chat UI            | TBD — Next.js or plain HTML + SSE           | Phase 3   |
| Voice (optional)   | Whisper (STT) + ElevenLabs (TTS)           | Phase 3   |
| Hosting            | Run locally for the demo                    | Phase 4   |

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

---

## Session 1 Summary

**What we built:** A working hotel concierge agent — FastAPI backend, OpenAI-compatible tool use loop, 3 mock PMS tools, and a clean escalation handoff. All 3 test scenarios passing.

**What actually shipped:**

```
lingopal/
├── app/
│   ├── agent/concierge.py   ← agent loop + tool dispatch
│   ├── tools/mock_pms.py    ← 3 mock hotel tools + escalation
│   └── main.py              ← FastAPI /chat endpoint
├── test_agent.py            ← 3 terminal test scenarios
└── requirements.txt
```

**Test results:**

| Scenario | Result |
|---|---|
| Reservation lookup + suite upgrade | Passed — found reservation, approved upgrade |
| Late checkout (2pm) | Passed — denied, suggested front desk |
| Complaint → escalation | Passed — immediate handoff with context |

**Decisions made:**
- Switched from Anthropic SDK → OpenAI-compatible client so we can swap models freely
- Landed on Gemini (free tier via AI Studio) after OpenRouter free models were rate-limited or unavailable
- Kept mock PMS as plain Python dicts — no database needed for a demo

**One bug fixed:** `message.content` returns `None` on some model responses after tool calls. Guarded with `or ""`.

---

## Session 1 Diagram — What Actually Runs

```
test_agent.py
      │
      ▼
chat(history, message)        ← app/agent/concierge.py
      │
      ▼
Gemini 3.6 Flash              ← via OpenAI-compatible API
(openrouter.ai or
 generativelanguage.googleapis.com)
      │
      ├── tool_call: lookup_reservation
      ├── tool_call: request_upgrade
      ├── tool_call: request_early_late_checkout
      └── tool_call: escalate_to_human
              │
              ▼
       mock_pms.py            ← returns fake JSON
              │
              ▼
       result injected back into conversation history
              │
              ▼
       model generates final response
```

---

## Takeaway

The agent loop itself is simple — the hard part is the edge cases. Model returns `None`? Guard it. Free tier rate limits? Have a backup model. Tool logic wrong? Write a test that catches it before you demo.

The escalation path is the one thing you can't skip. It's the first question every enterprise buyer asks. Get that working cleanly and the rest is polish.
