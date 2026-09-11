"""
Quick terminal test — runs 3 scenarios without the HTTP layer.
Run: python test_agent.py
"""

from app.agent.concierge import chat

SCENARIOS = [
    [
        "Hi, I'd like to look up my reservation. My name is Alice Chen.",
        "Can I get a suite upgrade?",
    ],
    [
        "I'm Bob Tanaka. Can I check out at 2pm tomorrow?",
    ],
    [
        "I want a refund. The room was terrible.",
    ],
]


def run_scenario(name: str, messages: list[str]):
    print(f"\n{'='*50}")
    print(f"SCENARIO: {name}")
    print('='*50)
    history = []
    for msg in messages:
        print(f"\nGuest: {msg}")
        response, history = chat(history, msg)
        print(f"Agent:  {response}")


if __name__ == "__main__":
    run_scenario("Reservation lookup + upgrade", SCENARIOS[0])
    run_scenario("Late checkout request", SCENARIOS[1])
    run_scenario("Complaint → escalation", SCENARIOS[2])
