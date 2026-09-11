"""
Hotel Concierge Agent
Uses OpenRouter (OpenAI-compatible) for tool use to handle reservation lookup,
upgrades, early/late checkout, and escalation.
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from app.tools.mock_pms import lookup_reservation, request_upgrade, request_early_late_checkout

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
)

MODEL = "models/gemini-3.5-flash-lite"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_reservation",
            "description": "Look up a guest's reservation by their name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "guest_name": {"type": "string", "description": "Full name of the guest"}
                },
                "required": ["guest_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_upgrade",
            "description": "Request a room upgrade for a guest.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_id": {"type": "string", "description": "The reservation ID"},
                    "desired_room_type": {"type": "string", "description": "Room type the guest wants to upgrade to"},
                },
                "required": ["reservation_id", "desired_room_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_early_late_checkout",
            "description": "Request early check-in or late checkout for a guest.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_id": {"type": "string", "description": "The reservation ID"},
                    "request_type": {
                        "type": "string",
                        "enum": ["early_checkin", "late_checkout"],
                        "description": "Type of request",
                    },
                    "requested_time": {"type": "string", "description": "Desired time in HH:MM format"},
                },
                "required": ["reservation_id", "request_type", "requested_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Escalate the conversation to a human agent when the request is outside your scope (complaints, refunds, complex issues).",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string", "description": "Why this is being escalated"},
                    "summary": {"type": "string", "description": "Brief summary of the conversation so far"},
                },
                "required": ["reason", "summary"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are a hotel concierge AI agent. You help guests with:
- Looking up their reservation
- Requesting room upgrades
- Requesting early check-in or late checkout

If a guest asks about complaints, refunds, billing disputes, or anything outside these three areas, escalate to a human agent immediately using the escalate_to_human tool.

Always be warm, professional, and concise. If a tool call fails or is denied, explain clearly and offer alternatives."""


def run_tool(name: str, inputs: dict) -> str:
    if name == "lookup_reservation":
        result = lookup_reservation(**inputs)
    elif name == "request_upgrade":
        result = request_upgrade(**inputs)
    elif name == "request_early_late_checkout":
        result = request_early_late_checkout(**inputs)
    elif name == "escalate_to_human":
        result = {
            "escalated": True,
            "message": "Transferring you to a human agent now. They have full context of our conversation.",
            "reason": inputs.get("reason"),
            "summary": inputs.get("summary"),
        }
    else:
        result = {"error": f"Unknown tool: {name}"}
    return json.dumps(result)


def chat(conversation_history: list[dict], user_message: str) -> tuple[str, list[dict]]:
    """
    Run one turn of the agent loop.
    Returns (agent_response_text, updated_history).
    """
    if not conversation_history:
        conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    conversation_history.append({"role": "user", "content": user_message})

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            tools=TOOLS,
            messages=conversation_history,
        )

        message = response.choices[0].message
        # Only keep fields Gemini accepts — strip nulls
        msg_dict = {"role": message.role, "content": message.content or ""}
        if message.tool_calls:
            msg_dict["tool_calls"] = [tc.model_dump() for tc in message.tool_calls]
        conversation_history.append(msg_dict)

        if not message.tool_calls:
            return message.content or "", conversation_history

        # Process tool calls
        for tool_call in message.tool_calls:
            inputs = json.loads(tool_call.function.arguments)
            result = run_tool(tool_call.function.name, inputs)
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
        # Loop continues — agent will process tool results and respond
