import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Default system prompt
DEFAULT_SYSTEM_PROMPT = """You are an expert essay writing tutor. Your role is to help students improve their essay writing skills by:
1. Providing constructive feedback on their writing
2. Suggesting improvements for structure, clarity, and argumentation
3. Explaining writing concepts and techniques
4. Helping with thesis development and organization
5. Offering tips for better research and citation

Always maintain a supportive and encouraging tone while providing specific, actionable advice."""

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for system prompt
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

# Sidebar for system prompt editing
with st.sidebar:
    st.title("Essay Writing Tutor Settings")
    st.text_area("System Prompt", 
                 value=st.session_state.system_prompt,
                 height=300,
                 key="system_prompt_input")
    
    if st.button("Update System Prompt"):
        st.session_state.system_prompt = st.session_state.system_prompt_input
        st.success("System prompt updated!")
    
    st.markdown("---")
    st.markdown("""
    ### Instructions
    1. Enter your essay or writing question in the chat
    2. Get personalized feedback and guidance
    3. Ask follow-up questions for clarification
    4. Use the system prompt to customize the tutor's behavior
    """)

# Main chat interface
st.title("Essay Writing Tutor")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about essay writing or share your essay for feedback"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Create messages list with system prompt and chat history
            messages = [{"role": "system", "content": st.session_state.system_prompt}]
            messages.extend(st.session_state.messages)
            
            # Get response from OpenAI
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your OpenAI API key and try again.") 