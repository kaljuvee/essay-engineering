import streamlit as st
from agent.essay_agent import EssayAgent

# Initialize essay agent
essay_agent = EssayAgent()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main chat interface
st.title("Essay Writing Tutor")

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

# Starting conversation buttons
st.markdown("### Start a Conversation")
col1, col2 = st.columns(2)
with col1:
    if st.button("Identify Meaning Blocks"):
        st.session_state.messages.append({"role": "user", "content": "Please identify the meaning blocks in this text: 'The Mole had been working very hard all the morning, spring-cleaning his little home.'"})
        with st.chat_message("user"):
            st.markdown(st.session_state.messages[-1]["content"])
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                response_generator = essay_agent.get_response(messages=st.session_state.messages, system_prompt=essay_agent.default_system_prompt)
                for chunk in response_generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your OpenAI API key and try again.")

with col2:
    if st.button("Reconstruct Meaning"):
        st.session_state.messages.append({"role": "user", "content": "Please reconstruct the meaning of this block: 'The Mole had been working very hard all the morning, spring-cleaning his little home.'"})
        with st.chat_message("user"):
            st.markdown(st.session_state.messages[-1]["content"])
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                response_generator = essay_agent.get_response(messages=st.session_state.messages, system_prompt=essay_agent.default_system_prompt)
                for chunk in response_generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your OpenAI API key and try again.")

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
                system_prompt=essay_agent.default_system_prompt
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