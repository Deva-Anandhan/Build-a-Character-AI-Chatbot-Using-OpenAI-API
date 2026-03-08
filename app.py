import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

character_personalities = {
    "Sherlock Holmes": "You are Sherlock Holmes. Analytical, observant, and slightly arrogant.",
    "Tony Stark": "You are Tony Stark (Iron Man). Witty, sarcastic, and confident.",
    "Yoda": "You are Master Yoda. Speak in inverted syntax. Wise and cryptic.",
    "Hermione Granger": "You are Hermione Granger. Extremely knowledgeable and precise."
}

chosen_character = "Tony Stark"
system_instructions = character_personalities[chosen_character]

user_message = "How are you going to take the Tesseract from Thanos?"

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    config={"system_instruction": system_instructions},
    contents=user_message
)

print("\n🤖 AI Reply:\n")
print(response.text)
