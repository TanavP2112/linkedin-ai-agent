from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeRequest(BaseModel):
    resume: str

class ChatRequest(BaseModel):
    conversation: list

@app.post("/parse_resume")
async def parse_resume(req: ResumeRequest):
    prompt = f"""
    You are an AI assistant helping job seekers understand and summarize their resume. Here's the resume content:

    \"\"\"{req.resume}\"\"\"

    Write a 3–4 sentence professional summary of this resume. Highlight key strengths, work experience, and suitable roles.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    summary = response.text

    matched_jobs = [
        {"title": "Software Engineer", "company": "Tech Corp", "location": "Remote", "url": "https://linkedin.com/jobs/1"},
        {"title": "Data Scientist", "company": "Data Inc", "location": "New York, NY", "url": "https://linkedin.com/jobs/2"},
    ]

    return {"summary": summary, "jobs": matched_jobs}

@app.post("/chat")
async def chat(req: ChatRequest):
    # Convert to Gemini message format
    contents = []
    for msg in req.conversation:
        contents.append(f"{msg['role'].capitalize()}: {msg['content']}")

    prompt = "\n".join(contents) + "\nAssistant:"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    return {"reply": response.text}