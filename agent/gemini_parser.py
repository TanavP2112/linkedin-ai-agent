from google import genai

def parse_gemini_response(response):
    client = genai.Client(api_key="GEMINI_API_KEY")