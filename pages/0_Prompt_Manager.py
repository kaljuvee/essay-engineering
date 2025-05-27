import streamlit as st
import os

def save_prompt(content: str):
    """Save the prompt to system_prompt.md."""
    with open("prompts/system_prompt.md", "w") as f:
        f.write(content)


def load_prompt():
    """Load the current prompt from system_prompt.md."""
    if os.path.exists("prompts/system_prompt.md"):
        with open("prompts/system_prompt.md", "r") as f:
            return f.read()
    return ""

def main():
    st.title("Prompt Manager (Single Version)")
    st.header("Edit System Prompt")

    current_prompt = load_prompt()
    new_prompt = st.text_area("System Prompt", value=current_prompt, height=400)

    if st.button("Save Prompt"):
        if new_prompt.strip():
            save_prompt(new_prompt)
            st.success("Prompt saved to prompts/system_prompt.md and will be used by the Essay Agent.")
        else:
            st.error("Prompt cannot be empty.")

if __name__ == "__main__":
    main()
