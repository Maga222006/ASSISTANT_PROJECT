from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Assistant Project API")

class Message(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Assistant Project API"}

@app.post("/chat")
async def chat(message: Message):
    return {"response": f"You said: {message.text}"}
