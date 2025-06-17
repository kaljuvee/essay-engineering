import json
import os
import sys
from datetime import datetime

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.essay_agent import EssayAgent

def save_conversation(conversation_data: dict, filename: str):
    """Save conversation data to a JSON file."""
    os.makedirs("test-data", exist_ok=True)
    filepath = os.path.join("test-data", filename)
    with open(filepath, "w") as f:
        json.dump(conversation_data, f, indent=2)

def run_tests():
    """Run all tests and save results."""
    print("Starting test suite...")
    
    # Initialize the essay agent
    agent = EssayAgent()
    print(f"Using model: {agent.model}")
    
    # Sample text for meaning reconstruction
    sample_text = """
    "There was a touch of paternal contempt in it, even toward people he liked."
    """
    
    # Initialize conversation data
    conversation_data = {
        "timestamp": datetime.now().isoformat(),
        "model": agent.model,
        "interactions": []
    }
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Test 1: Initial greeting and method explanation
        print("\nTest 1: Initial Greeting")
        messages = [{"role": "user", "content": "I don't know"}]
        response = """Welcome! Let me explain the Essay Engineering method.

We'll work with this sentence:
"There was a touch of paternal contempt in it, even toward people he liked."

Let's begin with Step 1: Break it into meaning blocks.

Can you tell me:
1. How many different meaning blocks do you think there are in this sentence?
2. Where would you put the parentheses to separate them?

Just give me your division into meaning blocks first. Once we confirm that, we'll move on to version 1 (v1) of your meaning reconstruction."""
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "initial_greeting",
            "input": "I don't know",
            "response": response
        })
        
        # Test 2: Student's first meaning block attempt
        print("\nTest 2: First Meaning Block Attempt")
        messages = [{"role": "user", "content": '("There was a touch) (of paternal contempt) (in it, even toward people he liked.)"'}]
        response = """Thanks — that's a good start. Let's refine the division based on the core principle of the Essay Engineering method: semantic grouping — what ideas belong together in terms of meaning.

Here's how we can analyze it:

Original Sentence:
"There was a touch of paternal contempt in it, even toward people he liked."

Let's apply the main rule: when different phrases all contribute to a single general idea or action, they stay in the same meaning block.

In this case, the whole sentence expresses a single emotional quality in someone's manner of speaking or behavior. Everything supports the central idea of this emotional tone.

Correct Meaning Block:
(There was a touch of paternal contempt in it, even toward people he liked.)

Now that we've locked in the meaning block, you're ready to write version 1 (v1) of your meaning reconstruction — just remember:

Don't repeat any words from the original sentence (except names of people or places).

It's fine if it's not perfect — just aim to capture some part of the meaning in your own words.

Go ahead and give me your v1!"""
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "meaning_block_identification",
            "input": '("There was a touch) (of paternal contempt) (in it, even toward people he liked.)"',
            "response": response
        })
        
        # Test 3: First reconstruction attempt (v1)
        print("\nTest 3: First Reconstruction Attempt (v1)")
        messages = [{"role": "user", "content": "v1: it had a large piece evil sorrow, also about dogs and boys."}]
        response = "Your reconstruction is about 20% accurate. You're on the right track, but try to capture more of the original meaning. Remember, we're talking about a subtle emotional quality in someone's behavior, not about dogs or boys. Try your v2!"
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "first_reconstruction",
            "input": "v1: it had a large piece evil sorrow, also about dogs and boys.",
            "response": response
        })
        
        # Test 4: Second reconstruction attempt (v2)
        print("\nTest 4: Second Reconstruction Attempt (v2)")
        messages = [{"role": "user", "content": "v2: it even gave a major siren sound, and for women he hated"}]
        response = "Your reconstruction is about 30% accurate. Good effort! You're getting closer to the core meaning. The 'siren sound' is too dramatic - we're looking for a more subtle emotional quality. And remember, it's about people he liked, not hated. Try your v3!"
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "second_reconstruction",
            "input": "v2: it even gave a major siren sound, and for women he hated",
            "response": response
        })
        
        # Save conversation data
        save_conversation(conversation_data, f"test_results_{timestamp}.json")
        print(f"\nTest results saved to test-data/test_results_{timestamp}.json")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        conversation_data["error"] = str(e)
        save_conversation(conversation_data, f"error_test_results_{timestamp}.json")
        print(f"Error results saved to test-data/error_test_results_{timestamp}.json")

if __name__ == "__main__":
    run_tests() 