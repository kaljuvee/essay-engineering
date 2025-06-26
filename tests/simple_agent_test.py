#!/usr/bin/env python3
"""
Test script for the SimpleEssayAgent
Simulates the essay engineering workflow with practice inputs and outputs
"""

import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add the parent directory to the path so we can import the agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.simple_essay_agent import SimpleEssayAgent

class SimpleAgentTester:
    def __init__(self):
        self.agent = SimpleEssayAgent()
        self.test_results = []
        
    def run_test_case(self, test_name: str, inputs: List[str], expected_behaviors: List[str]) -> Dict[str, Any]:
        """Run a single test case and return results"""
        print(f"\n=== Running Test: {test_name} ===")
        
        test_result = {
            "test_name": test_name,
            "timestamp": datetime.now().isoformat(),
            "inputs": inputs,
            "expected_behaviors": expected_behaviors,
            "actual_responses": [],
            "agent_state": [],
            "passed": True,
            "notes": []
        }
        
        # Reset agent for each test
        self.agent = SimpleEssayAgent()
        
        for i, user_input in enumerate(inputs):
            print(f"\nInput {i+1}: {user_input}")
            
            # Add message to agent
            self.agent.add_message("user", user_input)
            
            # Get agent response based on input
            response = self._get_agent_response(user_input)
            test_result["actual_responses"].append(response)
            
            print(f"Response: {response}")
            
            # Check if response matches expected behavior
            if i < len(expected_behaviors):
                expected = expected_behaviors[i]
                if expected.lower() in response.lower():
                    print(f"✅ Expected behavior '{expected}' found in response")
                else:
                    print(f"❌ Expected behavior '{expected}' not found in response")
                    test_result["passed"] = False
                    test_result["notes"].append(f"Expected '{expected}' not found in response")
            
            # Record agent state
            test_result["agent_state"].append({
                "current_sentence": self.agent.current_sentence,
                "meaning_blocks_count": len(self.agent.meaning_blocks),
                "versions_count": len(self.agent.versions),
                "conversation_length": len(self.agent.conversation_history)
            })
        
        return test_result
    
    def _get_agent_response(self, user_input: str) -> str:
        """Get appropriate response from agent based on input"""
        if not self.agent.current_sentence:
            # First input - treat as new sentence
            self.agent.current_sentence = user_input
            return f"Great! Let's analyze this sentence: '{user_input}'\n\nCan you break it into meaning blocks? Use parentheses to separate them, like: (block 1) (block 2)"
        
        elif "(" in user_input and ")" in user_input:
            # User is providing meaning blocks
            blocks = self.agent.analyze_meaning_blocks(user_input)
            return f"Thanks for your meaning blocks! I see you've identified {len(blocks)} blocks. Now try creating version 1 (v1) of your meaning reconstruction. Remember not to repeat words from the original."
        
        elif user_input.lower().startswith("v") and any(char.isdigit() for char in user_input):
            # User is providing a version
            version_num = len(self.agent.versions) + 1
            self.agent.create_version(version_num, user_input)
            return self.agent.get_next_prompt()
        
        elif "evaluate" in user_input.lower() or "accuracy" in user_input.lower():
            # User wants evaluation
            if self.agent.versions:
                last_version = self.agent.versions[-1]
                return f"Looking at {last_version}, I can see you're making progress. Let's continue improving. Try the next version!"
            else:
                return "I don't see any versions to evaluate yet. Please provide a version first."
        
        else:
            # Default response
            return "I understand. Please provide meaning blocks or a version to continue."

def main():
    tester = SimpleAgentTester()
    
    # Test cases based on the essay engineering workflow
    test_cases = [
        {
            "name": "Complete Essay Engineering Workflow",
            "inputs": [
                "There was a touch of paternal contempt in it, even toward people he liked.",
                "(There was a touch of paternal contempt) (in it, even toward people he liked)",
                "v1. it had a large piece evil sorrow, also about dogs and boys",
                "v2. it even gave a major siren sound, and for women he hated",
                "v3. it even had a little piece of monster man, also for acceptable girlfriends",
                "v4. it even had a little bit of bossy professor, also for men and women he knew",
                "v5. it even had a little bit of bossy anger, also for men and women he thought were good"
            ],
            "expected_behaviors": [
                "analyze this sentence",
                "meaning blocks",
                "version 1",
                "version 2", 
                "version 3",
                "version 4",
                "version 5"
            ]
        },
        {
            "name": "Meaning Block Analysis Only",
            "inputs": [
                "The Mole had been working very hard all the morning, spring-cleaning his little home.",
                "(The Mole had been working very hard) (all the morning) (spring-cleaning his little home)"
            ],
            "expected_behaviors": [
                "analyze this sentence",
                "meaning blocks"
            ]
        },
        {
            "name": "Version Creation Without Meaning Blocks",
            "inputs": [
                "Hello, I want to create a version",
                "v1. this is my first attempt"
            ],
            "expected_behaviors": [
                "analyze this sentence",
                "version 1"
            ]
        },
        {
            "name": "Evaluation Request",
            "inputs": [
                "Please evaluate my work",
                "v1. my reconstruction attempt",
                "evaluate this version"
            ],
            "expected_behaviors": [
                "analyze this sentence",
                "version 1",
                "making progress"
            ]
        }
    ]
    
    # Run all test cases
    for test_case in test_cases:
        result = tester.run_test_case(
            test_case["name"],
            test_case["inputs"], 
            test_case["expected_behaviors"]
        )
        tester.test_results.append(result)
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"test-data/simple-agent-test-{timestamp}.json"
    
    # Ensure test-data directory exists
    os.makedirs("test-data", exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({
            "test_run": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(tester.test_results),
                "passed_tests": sum(1 for r in tester.test_results if r["passed"]),
                "failed_tests": sum(1 for r in tester.test_results if not r["passed"])
            },
            "results": tester.test_results
        }, f, indent=2)
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Total tests: {len(tester.test_results)}")
    print(f"Passed: {sum(1 for r in tester.test_results if r['passed'])}")
    print(f"Failed: {sum(1 for r in tester.test_results if not r['passed'])}")
    print(f"Results saved to: {output_file}")
    
    # Print detailed results
    for result in tester.test_results:
        status = "✅ PASSED" if result["passed"] else "❌ FAILED"
        print(f"{status}: {result['test_name']}")
        if result["notes"]:
            for note in result["notes"]:
                print(f"  Note: {note}")

if __name__ == "__main__":
    main()
