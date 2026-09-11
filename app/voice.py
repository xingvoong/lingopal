"""
ElevenLabs TTS — converts agent text response to audio.
"""

import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # George — clear, professional
MODEL_ID = "eleven_multilingual_v2"


def text_to_speech(text: str) -> bytes:
    audio = _client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id=MODEL_ID,
    )
    return b"".join(audio)
