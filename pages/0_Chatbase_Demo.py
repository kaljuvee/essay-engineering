import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(
        page_title="Chatbase Chatbot Demo",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Chatbase Chatbot Demo")
    st.markdown("---")
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### Welcome to the Chatbase Chatbot Demo!
        
        This page demonstrates how to embed a Chatbase chatbot in a Streamlit application.
        The chatbot widget will appear in the bottom right corner of your browser.
        
        **Instructions:**
        1. Look for the chat widget in the bottom right corner
        2. Click on it to start a conversation
        3. Test the chatbot with your questions
        """)
        
        # Add some spacing
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Display a placeholder or additional info
        st.info("💡 **Tip:** The chatbot is embedded using HTML components and will work across different browsers and devices.")
    
    # Embed the Chatbase chatbot using HTML components
    chatbase_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chatbase Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }
        </style>
    </head>
    <body>
        <!-- Chatbase Embed Code -->
        <script src="https://www.chatbase.co/embed.min.js" defer></script>
        <script>
            window.chatbaseConfig = { chatbotId: "J0U6mLwA-v1klk_NMqqc4" };
        </script>
    </body>
    </html>
    """
    
    # Embed the HTML component
    components.html(chatbase_html, height=0, scrolling=False)
    
    # Add footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Powered by <a href='https://www.chatbase.co' target='_blank'>Chatbase</a> and <a href='https://streamlit.io' target='_blank'>Streamlit</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
