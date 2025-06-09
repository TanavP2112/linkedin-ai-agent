import streamlit as st
import os
from dotenv import load_dotenv

from agent.resume_parser import parse_resume
from agent.gemini_parser import parse_gemini_response
from agent.job_scraper import linkedin_search
from chatbot import chat

load_dotenv()

st.set_page_config(page_title="LinkedIn Job Search Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_info" not in st.session_state:
    st.session_state.resume_info = {}

st.title("LinkedIn Job Search Agent")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    with open("tmp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("Resume uploaded successfully!")
    resume_text = parse_resume("temp_resume.pdf")
    resume_info = parse_gemini_response(resume_text)
    st.session_state.resume_text = resume_text
    st.session_state.resume_info = resume_info
    st.write("Resume Text:")
    st.write(resume_text)
    st.write("Extracted Resume Information:")
    st.write(resume_info)

st.text("Hello! How may I help you on your job search today?")
user_input = st.text_input("You:", key="user_input")