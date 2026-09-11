"""
FastAPI server for the Hotel Concierge Agent.
POST /chat  — stateless endpoint, caller manages conversation history.
POST /speak — converts text to speech via ElevenLabs, returns audio.
GET  /      — serves the voice UI.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.agent.concierge import chat
from app.voice import text_to_speech

app = FastAPI(title="Hotel Concierge Agent")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    response: str
    history: list[dict]


class SpeakRequest(BaseModel):
    text: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    response_text, updated_history = chat(req.history, req.message)
    return ChatResponse(response=response_text, history=updated_history)


@app.post("/speak")
async def speak_endpoint(req: SpeakRequest):
    audio = text_to_speech(req.text)
    return Response(content=audio, media_type="audio/mpeg")


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("app/static/index.html") as f:
        return f.read()


@app.get("/health")
async def health():
    return {"status": "ok"}
