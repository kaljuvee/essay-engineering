import streamlit as st
import requests
import os

# Allow user to select API endpoint or use environment variable
API_OPTIONS = [
    "https://essay-engineering.onrender.com/chat",
    "http://localhost:8001/chat"
]

def get_api_url():
    return os.environ.get("ESSAY_ENGINEERING_API_URL") or st.session_state.get("api_url") or API_OPTIONS[0]

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

# Move API endpoint selection to sidebar
st.sidebar.title("Settings")
if "api_url" not in st.session_state:
    st.session_state.api_url = API_OPTIONS[0]
api_url = st.sidebar.selectbox(
    "Select API Endpoint",
    API_OPTIONS,
    index=API_OPTIONS.index(st.session_state.api_url) if st.session_state.api_url in API_OPTIONS else 0
)
st.session_state.api_url = api_url

# Add Refresh button to clear conversation
if st.sidebar.button("🔄 Refresh Conversation"):
    st.session_state.messages = []
    st.session_state.current_step = "intro"
    st.session_state.current_version = 0
    st.rerun()

st.title("Essay Engineering")

# Initialize session state for chat history and conversation state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_step" not in st.session_state:
    st.session_state.current_step = "intro"
if "current_version" not in st.session_state:
    st.session_state.current_version = 0

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
- When identifying meaning blocks, consider:
  - What is the main action or event?
  - Who is involved?
  - When does it happen?
  - Why or how is it happening?

**Reconstruction of Meaning:**
- Reconstruction involves explaining each meaning block in your own words.
- This process helps you internalize the text's nuances and improve your comprehension.
- You'll create multiple versions (v1, v2, v3, etc.) to improve your understanding.
- Remember: Don't repeat words from the original text (except names of people or places).

Try your hand at identifying meaning blocks and reconstructing their meaning using the practice text below.
""")

# Practice text
practice_text = '"There was a touch of paternal contempt in it, even toward people he liked."'

# Starting conversation buttons
st.markdown("### Practice Exercise")
st.markdown(f"**Practice Text:** {practice_text}")

col1, col2 = st.columns(2)
with col1:
    if st.button("Start Meaning Block Analysis"):
        st.markdown("""
        Let's begin with Step 1: Break it into meaning blocks.
        
        Can you tell me:
        1. How many different meaning blocks do you think there are in this sentence?
        2. Where would you put the parentheses to separate them?
        
        Just give me your division into meaning blocks first. Once we confirm that, we'll move on to version 1 (v1) of your meaning reconstruction.
        """)
        user_msg = {"role": "user", "content": "I don't know"}
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(user_msg["content"])
        with st.chat_message("assistant"):
            response = get_api_response(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    if st.button("Start Reconstruction"):
        st.markdown("""
        Now that we've identified the meaning blocks, let's start reconstructing the meaning.
        
        Give me your version 1 (v1) of the meaning reconstruction. Remember:
        - Don't repeat words from the original text
        - It's fine if it's not perfect
        - Just aim to capture some part of the meaning in your own words
        """)
        user_msg = {"role": "user", "content": "I'm ready to start my reconstruction"}
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(user_msg["content"])
        with st.chat_message("assistant"):
            response = get_api_response(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Chat input
if prompt := st.chat_input("Share your meaning blocks or reconstruction, or ask for help"):
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = get_api_response(st.session_state.messages)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response}) 