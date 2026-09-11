"""
FastAPI server for the Hotel Concierge Agent.
POST /chat — stateless endpoint, caller manages conversation history.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.concierge import chat

app = FastAPI(title="Hotel Concierge Agent")


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    response: str
    history: list[dict]


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    response_text, updated_history = chat(req.history, req.message)
    return ChatResponse(response=response_text, history=updated_history)


@app.get("/health")
async def health():
    return {"status": "ok"}
