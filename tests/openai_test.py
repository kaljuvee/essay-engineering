import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get the model name from environment variables
model = os.getenv("OPENAI_MODEL", "gpt-4o")
print(f"Model from .env: {model}")

# Simple test function to call the OpenAI API
def test_openai():
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ]
        )
        print(f"Response from {model}: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_openai()
