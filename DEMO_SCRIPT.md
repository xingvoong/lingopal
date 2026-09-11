# Demo Script — Hotel Concierge Agent

A 2-minute Loom walkthrough. Three scenarios, one reset between each.

---

## Setup (before recording)

1. Start the server: `source venv/bin/activate && uvicorn app.main:app --reload`
2. Open **http://localhost:8000** in Chrome
3. Have the browser tab and terminal side by side — or just the browser fullscreen
4. Do a quick mic test before hitting record

---

## Scenario 1 — Reservation Lookup + Upgrade (~40s)

**Say:** "Hi, my name is Alice Chen. Can you look up my reservation?"

- Agent finds the reservation and reads back the details
- **Say:** "Can I get a suite upgrade?"
- Agent approves the upgrade

**What this shows:** The agent calls two tools in sequence — lookup first, then upgrade. It's not just chatting, it's acting.

---

## Scenario 2 — Late Checkout (~20s)

Hit **Reset conversation**.

**Say:** "I'm Bob Tanaka. Can I check out at 2pm tomorrow?"

- Agent looks up Bob's reservation and processes the late checkout request
- Returns a clear approval or denial with next steps

**What this shows:** Multi-turn memory — the agent looked up the reservation on its own without being asked, then acted on the request.

---

## Scenario 3 — Escalation (~20s)

Hit **Reset conversation**.

**Say:** "I want a refund. The room was absolutely terrible."

- Agent immediately escalates — amber bubble appears
- ElevenLabs reads out the handoff message

**What this shows:** The agent knows its limits. It doesn't try to handle what it can't. Full context handoff — a human picking this up would know exactly what the guest said.

---

## Closing (optional ~20s)

Briefly show the code structure in the terminal or editor:

- `app/agent/concierge.py` — the tool loop
- `app/tools/mock_pms.py` — the 3 mock tools
- `app/voice.py` — ElevenLabs integration

**What you'd build next:** Real PMS integration, multilingual support (natural fit for Lingopal's translation stack), and a proper evaluation harness to measure resolution rate.

---

## Tips

- Speak clearly and slightly slower than normal — Web Speech API is sensitive
- If it mishears you, use the text input — don't fumble on camera
- Keep the escalation scenario last — it's the most impressive ending
