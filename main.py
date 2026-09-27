import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

print("GEMINI KEY EXISTS:", bool(GEMINI_API_KEY))


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

    if not GEMINI_API_KEY:
        return {
            "error": "GEMINI_API_KEY is missing"
        }

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

    try:
        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=60
        )

        result = response.json()

        if response.status_code != 200:
            return {
                "error": result,
                "status": response.status_code
            }

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return {
            "reply": reply
        }

    except Exception as e:
        return {
            "error": str(e)
    }
