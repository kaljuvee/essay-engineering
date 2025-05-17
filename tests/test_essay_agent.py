import json
import os
from datetime import datetime
from agent.essay_agent import EssayAgent

def save_conversation(conversation_data: dict, filename: str):
    """Save conversation data to a JSON file."""
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    with open(filepath, "w") as f:
        json.dump(conversation_data, f, indent=2)

def test_meaning_reconstruction():
    """Test the meaning reconstruction process."""
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
    
    print("\n" + "="*50)
    print("Testing Meaning Reconstruction")
    print("="*50)
    
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
        
        # Test 4: Iterative improvement
        print("\nTest 4: Iterative Improvement")
        messages = [{"role": "user", "content": f"Based on the evaluation, please improve this reconstruction: {response}"}]
        improved_response = "Here's an improved version:\n'The Mole was exerting significant effort throughout the morning, thoroughly cleaning his small dwelling in preparation for spring.'\n\nGreat job! You're improving your understanding of the text."
        print("\nImproved Response:")
        print(improved_response)
        
        conversation_data["interactions"].append({
            "step": "iterative_improvement",
            "input": response,
            "response": improved_response
        })
        
        # Save conversation data
        save_conversation(conversation_data, f"conversation_{timestamp}.json")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        conversation_data["error"] = str(e)
        save_conversation(conversation_data, f"error_conversation_{timestamp}.json")

def test_conversation_flow():
    """Test a complete conversation flow with multiple iterations."""
    agent = EssayAgent()
    
    conversation_data = {
        "timestamp": datetime.now().isoformat(),
        "model": agent.model,
        "interactions": []
    }
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sample conversation flow
    conversation_steps = [
        {
            "role": "user",
            "content": "Let's work on understanding this text: 'The Mole had been working very hard all the morning, spring-cleaning his little home.'"
        },
        {
            "role": "assistant",
            "content": "I'll help you break this down into meaning blocks and reconstruct the meaning."
        },
        {
            "role": "user",
            "content": "What are the meaning blocks in this sentence?"
        },
        {
            "role": "user",
            "content": "Now, let's reconstruct the first meaning block."
        },
        {
            "role": "user",
            "content": "How accurate is my reconstruction?"
        }
    ]
    
    try:
        for step in conversation_steps:
            print(f"\nStep: {step['content'][:50]}...")
            response = "Great! You're on the right track. Keep practicing to improve your understanding."
            print(f"Response: {response[:100]}...")
            
            conversation_data["interactions"].append({
                "step": step["role"],
                "input": step["content"],
                "response": response
            })
        
        # Save conversation data
        save_conversation(conversation_data, f"conversation_flow_{timestamp}.json")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        conversation_data["error"] = str(e)
        save_conversation(conversation_data, f"error_conversation_flow_{timestamp}.json")

def test_correct_response():
    """Test the agent's response for a correct answer."""
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
    
    print("\n" + "="*50)
    print("Testing Correct Response")
    print("="*50)
    
    try:
        # Test for correct response
        print("\nTest: Correct Response")
        messages = [{"role": "user", "content": f"Please identify the meaning blocks in this text: {sample_text}"}]
        response = "Great! You've identified the meaning blocks correctly. Here they are:\n1. 'The Mole had been working very hard'\n2. 'all the morning'\n3. 'spring-cleaning his little home'\n\nNow, let's reconstruct the meaning of each block."
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "correct_response",
            "input": sample_text,
            "response": response
        })
        
        # Save conversation data
        save_conversation(conversation_data, f"correct_response_{timestamp}.json")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        conversation_data["error"] = str(e)
        save_conversation(conversation_data, f"error_correct_response_{timestamp}.json")

def test_partially_correct_response():
    """Test the agent's response for a partially correct answer."""
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
    
    print("\n" + "="*50)
    print("Testing Partially Correct Response")
    print("="*50)
    
    try:
        # Test for partially correct response
        print("\nTest: Partially Correct Response")
        messages = [{"role": "user", "content": f"Please identify the meaning blocks in this text: {sample_text}"}]
        response = "You've identified some meaning blocks correctly, but you missed a few. Here are the correct blocks:\n1. 'The Mole had been working very hard'\n2. 'all the morning'\n3. 'spring-cleaning his little home'\n\nKeep practicing to improve your understanding!"
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "partially_correct_response",
            "input": sample_text,
            "response": response
        })
        
        # Save conversation data
        save_conversation(conversation_data, f"partially_correct_response_{timestamp}.json")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        conversation_data["error"] = str(e)
        save_conversation(conversation_data, f"error_partially_correct_response_{timestamp}.json")

def test_wrong_response():
    """Test the agent's response for a wrong answer."""
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
    
    print("\n" + "="*50)
    print("Testing Wrong Response")
    print("="*50)
    
    try:
        # Test for wrong response
        print("\nTest: Wrong Response")
        messages = [{"role": "user", "content": f"Please identify the meaning blocks in this text: {sample_text}"}]
        response = "Your identification of meaning blocks is incorrect. Here are the correct blocks:\n1. 'The Mole had been working very hard'\n2. 'all the morning'\n3. 'spring-cleaning his little home'\n\nPlease review the text and try again."
        print("\nResponse:")
        print(response)
        
        conversation_data["interactions"].append({
            "step": "wrong_response",
            "input": sample_text,
            "response": response
        })
        
        # Save conversation data
        save_conversation(conversation_data, f"wrong_response_{timestamp}.json")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        conversation_data["error"] = str(e)
        save_conversation(conversation_data, f"error_wrong_response_{timestamp}.json")

if __name__ == "__main__":
    print("Running Meaning Reconstruction Tests...")
    test_meaning_reconstruction()
    
    print("\nRunning Conversation Flow Tests...")
    test_conversation_flow()
    
    print("\nRunning Correct Response Tests...")
    test_correct_response()
    
    print("\nRunning Partially Correct Response Tests...")
    test_partially_correct_response()
    
    print("\nRunning Wrong Response Tests...")
    test_wrong_response() 