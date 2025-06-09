import streamlit as st
import requests
from pypdf import PdfReader

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
            response = requests.post("http://localhost:8000/parse_resume", json={"resume": text})
            if response.status_code == 200:
                data = response.json()
                st.subheader("Resume Summary:")
                st.write(data["summary"])

                st.subheader("Matched LinkedIn Jobs:")
                for job in data["jobs"]:
                    st.markdown(f"**{job['title']}** at *{job['company']}* — {job['location']}")
                    st.markdown(f"[View Job]({job['url']})")
            else:
                st.error(f"Error: {response.text}")

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
        response = requests.post("http://localhost:8000/chat", json={"conversation": st.session_state.conversation})
        # st.write("Response received from LinkedBot") <- debugging purposes only
        if response.status_code == 200:
            reply = response.json().get("reply", "")
            st.session_state.conversation.append({"role": "assistant", "content": reply})
        else:
            st.error(f"Error: {response.text}")
for msg in st.session_state.conversation:
    if msg["role"] == "user" and msg["content"].startswith("Resume Content:"):
        continue
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**LinkedBot:** {msg['content']}")
