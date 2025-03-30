import streamlit as st
from agent.essay_agent import EssayAgent

# Initialize essay agent
essay_agent = EssayAgent()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for system prompt
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = essay_agent.default_system_prompt

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
    st.markdown(f"### Current Model: {essay_agent.model}")
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
            # Get response from essay agent
            response_generator = essay_agent.get_response(
                messages=st.session_state.messages,
                system_prompt=st.session_state.system_prompt
            )
            
            # Stream the response
            for chunk in response_generator:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your OpenAI API key and try again.") 