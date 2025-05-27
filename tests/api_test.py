import requests

API_URL = "http://localhost:8001/chat"

# Test cases similar to those in test_essay_agent.py
sample_text = "The Mole had been working very hard all the morning, spring-cleaning his little home."

cases = [
    {
        "name": "Meaning Block Identification",
        "messages": [
            {"role": "user", "content": f"Please identify the meaning blocks in this text: {sample_text}"}
        ]
    },
    {
        "name": "First Reconstruction Attempt",
        "messages": [
            {"role": "user", "content": f"Please reconstruct the meaning of this block: {sample_text}"}
        ]
    },
    {
        "name": "Accuracy Evaluation",
        "messages": [
            {"role": "user", "content": "Please evaluate the accuracy of this reconstruction: The Mole was exerting significant effort throughout the morning, thoroughly cleaning his small dwelling."}
        ]
    },
    {
        "name": "Iterative Improvement",
        "messages": [
            {"role": "user", "content": "Based on the evaluation, please improve this reconstruction: The Mole was exerting significant effort throughout the morning, thoroughly cleaning his small dwelling."}
        ]
    },
]

def run_tests():
    for case in cases:
        print(f"\n=== {case['name']} ===")
        response = requests.post(API_URL, json={"messages": case["messages"]})
        if response.ok:
            print("Response:", response.json().get("response", "<no response field>"))
        else:
            print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    run_tests() 