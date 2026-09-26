from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
    return {
        "reply": "မင်းပြောတာကို လက်ခံရရှိပြီ။ AI system ကို ဆက်တည်ဆောက်နေတယ်။"
    }
