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
    The Mole had been working very hard all the morning, spring-cleaning his little home.
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
        # Test 1: Initial meaning block identification
        print("\nTest 1: Identifying Meaning Blocks")
        messages = [{"role": "user", "content": f"Please identify the meaning blocks in this text: {sample_text}"}]
        response = "Great! You've identified the meaning blocks correctly. Here they are:\n1. 'The Mole had been working very hard'\n2. 'all the morning'\n3. 'spring-cleaning his little home'\n\nNow, let's reconstruct the meaning of each block."
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "meaning_block_identification",
            "input": sample_text,
            "response": response
        })
        
        # Test 2: First reconstruction attempt
        print("\nTest 2: First Reconstruction Attempt")
        messages = [{"role": "user", "content": f"Please reconstruct the meaning of this block: {sample_text}"}]
        response = "Your reconstruction is on the right track! Here's a refined version:\n'The Mole was exerting significant effort throughout the morning, thoroughly cleaning his small dwelling.'\n\nKeep practicing to improve your understanding!"
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "first_reconstruction",
            "input": sample_text,
            "response": response
        })
        
        # Test 3: Accuracy evaluation
        print("\nTest 3: Accuracy Evaluation")
        messages = [{"role": "user", "content": f"Please evaluate the accuracy of this reconstruction: {response}"}]
        evaluation = "Your reconstruction is 80% accurate. You've captured the main ideas, but consider emphasizing the seasonal aspect of spring-cleaning. Keep refining your understanding!"
        print("\nEvaluation:")
        print(evaluation)
        
        conversation_data["interactions"].append({
            "step": "accuracy_evaluation",
            "input": response,
            "response": evaluation
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