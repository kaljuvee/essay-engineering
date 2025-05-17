import streamlit as st
import os
from datetime import datetime
import shutil

def save_prompt_version(content: str):
    """Save a new version of the prompt with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_dir = "prompts/versions"
    os.makedirs(version_dir, exist_ok=True)
    
    filename = f"{version_dir}/prompt_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(content)
    return filename

def get_prompt_versions():
    """Get list of all prompt versions."""
    version_dir = "prompts/versions"
    if not os.path.exists(version_dir):
        return []
    
    versions = []
    for file in os.listdir(version_dir):
        if file.endswith(".md"):
            timestamp = file.replace("prompt_", "").replace(".md", "")
            try:
                dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                versions.append((file, dt.strftime("%Y-%m-%d %H:%M:%S")))
            except ValueError:
                continue
    return sorted(versions, key=lambda x: x[1], reverse=True)

def activate_prompt(version_file: str):
    """Activate a specific prompt version as the current system prompt."""
    version_path = os.path.join("prompts/versions", version_file)
    if os.path.exists(version_path):
        shutil.copy2(version_path, "prompts/system_prompt.md")
        return True
    return False

def main():
    st.title("Prompt Manager")
    
    # Create tabs for different functions
    tab1, tab2 = st.tabs(["Create New Version", "Manage Versions"])
    
    with tab1:
        st.header("Create New Prompt Version")
        current_prompt = ""
        if os.path.exists("prompts/system_prompt.md"):
            with open("prompts/system_prompt.md", "r") as f:
                current_prompt = f.read()
        
        new_prompt = st.text_area("Edit Prompt", value=current_prompt, height=400)
        if st.button("Save New Version"):
            if new_prompt.strip():
                filename = save_prompt_version(new_prompt)
                st.success(f"New version saved: {filename}")
            else:
                st.error("Prompt cannot be empty")
    
    with tab2:
        st.header("Manage Prompt Versions")
        versions = get_prompt_versions()
        
        if versions:
            version_options = [f"{v[1]} - {v[0]}" for v in versions]
            selected_version = st.selectbox(
                "Select a version to activate",
                version_options,
                format_func=lambda x: x.split(" - ")[0]
            )
            
            if st.button("Activate Selected Version"):
                version_file = selected_version.split(" - ")[1]
                if activate_prompt(version_file):
                    st.success("Selected version activated as current system prompt")
                else:
                    st.error("Failed to activate version")
        else:
            st.info("No prompt versions found")

if __name__ == "__main__":
    main()
