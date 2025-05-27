import streamlit as st
import requests
import os

# Allow user to select API endpoint or use environment variable
API_OPTIONS = [
    "http://localhost:8001/chat",
    "https://essay-engineering.onrender.com/chat"
]
def get_api_url():
    return os.environ.get("ESSAY_ENGINEERING_API_URL") or st.session_state.get("api_url") or API_OPTIONS[0]

st.title("Essay Writing Tutor (API Mode)")

# API endpoint selection
if "api_url" not in st.session_state:
    st.session_state.api_url = API_OPTIONS[0]
api_url = st.selectbox("Select API Endpoint", API_OPTIONS, index=API_OPTIONS.index(st.session_state.api_url) if st.session_state.api_url in API_OPTIONS else 0)
st.session_state.api_url = api_url

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Instructions for meaning blocks and reconstruction
st.markdown("""
### Understanding Meaning Blocks and Reconstruction

**Meaning Blocks:**
- Meaning blocks are the core ideas or phrases in a text that carry significant information.
- Breaking down a text into meaning blocks helps you understand its structure and key points.
- Example: In the sentence "The Mole had been working very hard all the morning, spring-cleaning his little home," the meaning blocks are:
  1. "The Mole had been working very hard"
  2. "all the morning"
  3. "spring-cleaning his little home"

**Reconstruction of Meaning:**
- Reconstruction involves paraphrasing each meaning block to ensure you understand the text deeply.
- This process helps you internalize the text's nuances and improve your comprehension.
- Example: "The Mole had been working very hard" can be reconstructed as "The character was exerting significant effort."

Use the buttons below to practice identifying meaning blocks and reconstructing their meaning.
""")

# Helper to send messages to API
def get_api_response(messages):
    url = get_api_url()
    try:
        resp = requests.post(url, json={"messages": messages})
        if resp.ok:
            return resp.json().get("response", "<no response field>")
        else:
            return f"Error: {resp.status_code} {resp.text}"
    except Exception as e:
        return f"API request failed: {e}"

# Starting conversation buttons
st.markdown("### Start a Conversation")
col1, col2 = st.columns(2)
with col1:
    if st.button("Identify Meaning Blocks"):
        user_msg = {"role": "user", "content": "Please identify the meaning blocks in this text: 'The Mole had been working very hard all the morning, spring-cleaning his little home.'"}
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(user_msg["content"])
        with st.chat_message("assistant"):
            response = get_api_response(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    if st.button("Reconstruct Meaning"):
        user_msg = {"role": "user", "content": "Please reconstruct the meaning of this block: 'The Mole had been working very hard all the morning, spring-cleaning his little home.'"}
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(user_msg["content"])
        with st.chat_message("assistant"):
            response = get_api_response(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Chat input
if prompt := st.chat_input("Ask about essay writing or share your essay for feedback"):
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = get_api_response(st.session_state.messages)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response}) 