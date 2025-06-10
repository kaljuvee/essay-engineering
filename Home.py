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
    st.rerun()

st.title("Essay Engineering")

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
- Example: In the sentence "The Mole had been working very hard all the morning, spring-cleaning his little home," you might identify meaning blocks by asking:
  - Who is doing what?
  - When is it happening?
  - What specific action is being performed?

**Reconstruction of Meaning:**
- Reconstruction involves explaining each meaning block in your own words.
- This process helps you internalize the text's nuances and improve your comprehension.
- When reconstructing, consider:
  - What is the main action or event?
  - Who is involved?
  - When does it happen?
  - Why or how is it happening?

Try your hand at identifying meaning blocks and reconstructing their meaning using the practice text below.
""")

# Practice text
practice_text = "The Mole had been working very hard all the morning, spring-cleaning his little home."

# Starting conversation buttons
st.markdown("### Practice Exercise")
st.markdown(f"**Practice Text:** {practice_text}")

col1, col2 = st.columns(2)
with col1:
    if st.button("Share Your Meaning Blocks"):
        st.markdown("""
        Please identify the meaning blocks in the text above. Type your response in the chat below, 
        breaking the text into meaningful parts and explaining why you chose these blocks.
        """)
        user_msg = {"role": "user", "content": f"I think the meaning blocks in '{practice_text}' are:"}
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(user_msg["content"])

with col2:
    if st.button("Share Your Reconstruction"):
        st.markdown("""
        Please reconstruct the meaning of the text above. Type your response in the chat below, 
        explaining what you think each part means in your own words.
        """)
        user_msg = {"role": "user", "content": f"My reconstruction of '{practice_text}' is:"}
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(user_msg["content"])

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