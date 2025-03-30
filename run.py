from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from agent.essay_agent import EssayAgent
import uvicorn

app = FastAPI(
    title="Essay Writing Tutor API",
    description="API for essay writing assistance using OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

essay_agent = EssayAgent()

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
    system_prompt: Optional[str] = Field(None, description="Optional custom system prompt to override the default one")

    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "How do I write a good thesis statement?"
                    }
                ],
                "system_prompt": "You are a thesis statement expert. Focus only on thesis statements."
            }
        }

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI's response to the chat request")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Get essay writing assistance from the AI tutor.
    
    - **messages**: List of messages in the conversation
    - **system_prompt**: Optional custom system prompt to override the default one
    
    Returns:
        The AI's response to the chat request
    """
    try:
        response_generator = essay_agent.get_response(
            messages=[msg.dict() for msg in request.messages],
            system_prompt=request.system_prompt
        )
        return ChatResponse(response="".join(response_generator))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 