
import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"


class Message(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "name": "My AI Partner"
    }


@app.post("/chat")
def chat(data: Message):

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": data.message
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=body,
        timeout=60
    )

    result = response.json()

    if response.status_code != 200:
        return {
            "error": result
        }

    reply = result["candidates"][0]["content"]["parts"][0]["text"]

    return {
        "reply": reply
    }
