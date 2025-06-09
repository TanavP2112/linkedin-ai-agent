from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

def parse_gemini_response(resume):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"""
    You are an AI assistant extracting structured information from this resume text:

    \"\"\"
    {resume}
    \"\"\"

    Return ONLY a JSON with keys:
    - full_name
    - email
    - phone
    - education (list of degree, institution, year)
    - work_experience (list of role, company, years)
    - skills (comma separated)
    - desired_roles (list)
    - summary (1 sentence)

    JSON ONLY, no explanations.
    """
    response = client.generate_text(
        model="gemini-2.0-flash",
        prompt=prompt,
        response_format=genai.ResponseFormat.TEXT
    )
    return json.loads(response.text.strip())