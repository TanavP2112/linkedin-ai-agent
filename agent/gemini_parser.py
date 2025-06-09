from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key="GEMINI_API_KEY")

def parse_gemini_response(resume):
    prompt = f"""
    You are an AI assistant helping job seekers understand and summarize their resume. Here's the resume content:

    \"\"\"
    {resume}
    \"\"\"

    Please write a professional summary of this resume in 3–4 natural language sentences. Highlight strengths, work experience, and suitable job roles.
    """
    response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
    return response.text.strip()
