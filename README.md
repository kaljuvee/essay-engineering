# Essay Writing Tutor API

A FastAPI-based service that provides AI-powered essay writing assistance using OpenAI's API.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY='your-api-key-here'
OPENAI_MODEL='gpt-4-turbo-preview'  # or your preferred model
```

## Running the API Server

Start the FastAPI server with uvicorn:
```bash
# From the project root directory
python run.py
```

Or using uvicorn directly:
```bash
uvicorn run:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- Main API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

Run the test script:
```bash
# From the project root directory
python -m tests.test_essay_agent
```

## API Endpoints

### POST /chat

Send a message to get AI-powered essay writing help.

Example request:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I write a good thesis statement?"
    }
  ],
  "system_prompt": "You are a thesis statement expert. Focus only on thesis statements."
}
```

Example response:
```json
{
  "response": "A good thesis statement should be clear, concise, and arguable..."
}
```

## Development

The project structure:
```
.
├── agent/
│   ├── __init__.py
│   └── essay_agent.py
├── tests/
│   └── test_essay_agent.py
├── .env
├── requirements.txt
├── run.py
└── swagger.json
```