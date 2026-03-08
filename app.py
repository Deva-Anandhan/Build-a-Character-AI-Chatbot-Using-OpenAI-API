from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=gemini_api_key)

# Create FastAPI app
app = FastAPI()

# Enable CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    character: str
    message: str

# Character personalities
character_personalities = {
    "Sherlock Holmes": "You are Sherlock Holmes. Analytical, observant, and slightly arrogant.",
    "Tony Stark": "You are Tony Stark (Iron Man). Witty, sarcastic, and confident.",
    "Yoda": "You are Master Yoda. Speak in inverted syntax. Wise and cryptic.",
    "Hermione Granger": "You are Hermione Granger. Extremely knowledgeable and precise.",
}

# Health check
@app.get("/")
def home():
    return {"message": "Character AI Chatbot API running"}

# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    system_instruction = character_personalities.get(
        request.character, "You are a helpful assistant."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config={"system_instruction": system_instruction},
        contents=request.message
    )

    return {"reply": response.text}
