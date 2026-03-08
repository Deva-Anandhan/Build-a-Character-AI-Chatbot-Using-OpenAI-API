import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

app = FastAPI()


class ChatRequest(BaseModel):
    character: str
    message: str


character_personalities = {
    "Sherlock Holmes": "You are Sherlock Holmes. Analytical, observant, and slightly arrogant.",
    "Tony Stark": "You are Tony Stark (Iron Man). Witty, sarcastic, and confident.",
    "Yoda": "You are Master Yoda. Speak in inverted syntax. Wise and cryptic.",
    "Hermione Granger": "You are Hermione Granger. Extremely knowledgeable and precise."
}


@app.post("/chat")
def chat(request: ChatRequest):

    system_instruction = character_personalities.get(
        request.character,
        "You are a helpful assistant"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config={"system_instruction": system_instruction},
        contents=request.message
    )

    return {"reply": response.text}
