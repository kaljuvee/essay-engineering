import openai
from dotenv import load_dotenv
import os
from typing import List, Dict, Generator

class EssayAgent:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.default_system_prompt = """You are an expert essay writing tutor. Your role is to help students improve their essay writing skills by:
1. Providing constructive feedback on their writing
2. Suggesting improvements for structure, clarity, and argumentation
3. Explaining writing concepts and techniques
4. Helping with thesis development and organization
5. Offering tips for better research and citation

Always maintain a supportive and encouraging tone while providing specific, actionable advice."""

    def get_response(self, messages: List[Dict[str, str]], system_prompt: str = None) -> Generator[str, None, None]:
        """
        Get a streaming response from OpenAI.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            system_prompt: Optional system prompt to override the default one
            
        Yields:
            Chunks of the response as they arrive
            
        Raises:
            Exception: If messages list is empty or if OpenAI API call fails
        """
        if not messages:
            raise Exception("Messages list cannot be empty")
            
        try:
            # Create messages list with system prompt and chat history
            full_messages = [{"role": "system", "content": system_prompt or self.default_system_prompt}]
            full_messages.extend(messages)
            
            # Get response from OpenAI
            response = openai.chat.completions.create(
                model=self.model,
                messages=full_messages,
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
