import streamlit as st
import requests
from pypdf import PdfReader

BACKEND_URL = "https://linkedin-job-finder-wi5m.onrender.com"

st.title("LinkedIn Job Finder")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        text = uploaded_file.getvalue().decode("utf-8")

    st.session_state.resume_text = text

    st.text_area("Extracted Resume Text (note: this is how the AI will read your resume)", text, height=300)

    if st.button("Find Jobs"):
        with st.spinner("Parsing resume and finding jobs..."):
            try:
                response = requests.post(f"{BACKEND_URL}/parse_resume", json={"resume": text})
                response.raise_for_status()
                data = response.json()
                st.subheader("Resume Summary:")
                st.write(data["summary"])

                st.subheader("Matched LinkedIn Jobs:")
                for job in data["jobs"]:
                    st.markdown(f"**{job['title']}** at *{job['company']}* — {job['location']}")
                    st.markdown(f"[View Job]({job['url']})")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")

st.markdown("---")
st.header("LinkedIn Chatbot (LinkedBot)")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if (
    "resume_text" in st.session_state
    and not any("Resume Content:" in msg["content"] for msg in st.session_state.conversation)
):
    st.session_state.conversation.insert(0, {
        "role": "user",
        "content": f"Resume Content:\n{st.session_state.resume_text}"
    })

user_input = st.text_input("How may I help you today?")

if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})

    with st.spinner("Please Wait..."):
        try:
            response = requests.post(f"{BACKEND_URL}/chat", json={"conversation": st.session_state.conversation})
            response.raise_for_status()
            reply = response.json().get("reply", "")
            # st.write(f"Debug: Received reply: {reply}") <- debugging purposes ONLY
            st.session_state.conversation.append({"role": "assistant", "content": reply})
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

for msg in st.session_state.conversation:
    if msg["role"] == "user" and msg["content"].startswith("Resume Content:"):
        continue
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**LinkedBot:** {msg['content']}")
