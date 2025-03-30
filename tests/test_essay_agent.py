from agent.essay_agent import EssayAgent

def test_essay_agent():
    # Initialize the essay agent
    agent = EssayAgent()
    print(f"Using model: {agent.model}")
    
    # Sample questions to test
    questions = [
        "How do I write a good thesis statement?",
        "What's the best way to structure an argumentative essay?",
        "Can you help me improve my essay's introduction?"
    ]
    
    # Test each question
    for question in questions:
        print("\n" + "="*50)
        print(f"Question: {question}")
        print("="*50)
        
        try:
            # Get response
            messages = [{"role": "user", "content": question}]
            response = "".join(agent.get_response(messages))
            print("\nResponse:")
            print(response)
            
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_essay_agent() 