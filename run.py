from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from agent.simple_essay_agent import SimpleEssayAgent
import uvicorn

app = FastAPI(
    title="Essay Writing Tutor API",
    description="API for essay writing assistance using simple essay engineering",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize the simple essay agent
essay_agent = SimpleEssayAgent()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str = Field(..., description="The role of the message sender (user, assistant, or system)")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="List of messages in the conversation")

    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "There was a touch of paternal contempt in it, even toward people he liked."
                    }
                ]
            }
        }

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI's response to the chat request")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Get essay writing assistance from the simple essay engineering agent.
    
    - **messages**: List of messages in the conversation
    
    Returns:
        The AI's response to the chat request
    """
    try:
        # Process messages through the simple agent
        for msg in request.messages:
            essay_agent.add_message(msg.role, msg.content)
        
        # Get the latest user message
        latest_message = request.messages[-1].content
        
        # Simple logic to determine response based on content
        if "meaning blocks" in latest_message.lower() or "(" in latest_message and ")" in latest_message:
            # User is providing meaning blocks
            blocks = essay_agent.analyze_meaning_blocks(latest_message)
            response = f"Thanks for your meaning blocks! I see you've identified {len(blocks)} blocks. Now try creating version 1 (v1) of your meaning reconstruction. Remember not to repeat words from the original."
        
        elif latest_message.lower().startswith("v") and any(char.isdigit() for char in latest_message):
            # User is providing a version
            version_num = len(essay_agent.versions) + 1
            essay_agent.create_version(version_num, latest_message)
            response = essay_agent.get_next_prompt()
        
        elif "evaluate" in latest_message.lower() or "accuracy" in latest_message.lower():
            # User wants evaluation
            if essay_agent.versions:
                last_version = essay_agent.versions[-1]
                response = f"Looking at {last_version}, I can see you're making progress. Let's continue improving. Try the next version!"
            else:
                response = "I don't see any versions to evaluate yet. Please provide a version first."
        
        else:
            # Default response - treat as new sentence
            essay_agent.current_sentence = latest_message
            response = f"Great! Let's analyze this sentence: '{latest_message}'\n\nCan you break it into meaning blocks? Use parentheses to separate them, like: (block 1) (block 2)"
        
        return ChatResponse(response=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 