from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

def chat(message):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.chat(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": message}],
        response_format=genai.ResponseFormat.TEXT
    )
    return response.text.strip()
