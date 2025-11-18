"""
Mock Ollama Server for testing Google ADK agents.
Implements the Ollama API endpoints used by LiteLLM.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Literal
import json
import time
from datetime import datetime
import asyncio
import uvicorn

app = FastAPI(title="Mock Ollama Server", version="1.0.0")


# Request/Response Models
class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    options: Optional[Dict[str, Any]] = None


class ChatResponseMessage(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    model: str
    created_at: str
    message: ChatResponseMessage
    done: bool
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None


class ModelInfo(BaseModel):
    name: str
    modified_at: str
    size: int
    digest: str
    details: Dict[str, Any]


# Mock responses configuration
MOCK_RESPONSES = {
    "default": "This is a mock response from the Ollama server. Your agent is working correctly!",
    "joke": "Why do programmers prefer dark mode? Because light attracts bugs! 🐛"
}


def get_mock_response(messages: List[Message]) -> str:
    """Generate a mock response based on the conversation context."""
    last_message = messages[-1].content.lower() if messages else ""
    
    # Check for joke-related requests
    if any(word in last_message for word in ["joke", "funny", "humor", "laugh"]):
        return MOCK_RESPONSES["joke"]
    
    return MOCK_RESPONSES["default"]


async def generate_streaming_response(request: ChatRequest):
    """Generate a streaming response in Ollama format."""
    response_text = get_mock_response(request.messages)
    words = response_text.split()
    
    # Stream response word by word
    for i, word in enumerate(words):
        chunk = {
            "model": request.model,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "message": {
                "role": "assistant",
                "content": word + (" " if i < len(words) - 1 else "")
            },
            "done": False
        }
        yield json.dumps(chunk) + "\n"
        await asyncio.sleep(0.05)  # Simulate processing delay
    
    # Final chunk with done=True
    final_chunk = {
        "model": request.model,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "message": {
            "role": "assistant",
            "content": ""
        },
        "done": True,
        "total_duration": 1000000000,
        "load_duration": 100000000,
        "prompt_eval_count": len(request.messages),
        "prompt_eval_duration": 200000000,
        "eval_count": len(words),
        "eval_duration": 700000000
    }
    yield json.dumps(final_chunk) + "\n"


@app.post("/api/chat")
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    Handle chat completion requests.
    Supports both Ollama native format (/api/chat) and OpenAI-compatible format (/v1/chat/completions).
    """
    # Parse the request body manually to handle various formats
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Extract fields with defaults
    model = body.get("model", "test_model")
    messages = body.get("messages", [])
    stream = body.get("stream", False)
    
    # Convert messages to Message objects
    message_objects = [Message(**msg) for msg in messages]
    
    if stream:
        request_obj = ChatRequest(
            model=model,
            messages=message_objects,
            stream=stream,
            temperature=body.get("temperature", 0.7),
            top_p=body.get("top_p", 1.0),
            max_tokens=body.get("max_tokens"),
            options=body.get("options")
        )
        return StreamingResponse(
            generate_streaming_response(request_obj),
            media_type="application/x-ndjson"
        )
    
    # Non-streaming response
    response_text = get_mock_response(message_objects)
    
    response = ChatResponse(
        model=model,
        created_at=datetime.utcnow().isoformat() + "Z",
        message=ChatResponseMessage(
            role="assistant",
            content=response_text
        ),
        done=True,
        total_duration=1000000000,
        load_duration=100000000,
        prompt_eval_count=len(message_objects),
        prompt_eval_duration=200000000,
        eval_count=len(response_text.split()),
        eval_duration=700000000
    )
    
    return response


@app.get("/api/tags")
async def list_models():
    """List available models."""
    return {
        "models": [
            {
                "name": "test_model:latest",
                "modified_at": datetime.utcnow().isoformat() + "Z",
                "size": 4000000000,
                "digest": "mock_digest_123",
                "details": {
                    "format": "gguf",
                    "family": "llama",
                    "parameter_size": "7B",
                    "quantization_level": "Q4_0"
                }
            }
        ]
    }


@app.get("/api/show")
async def show_model(name: str):
    """Show model information."""
    return {
        "modelfile": "# Mock model",
        "parameters": "temperature 0.7\ntop_p 0.9",
        "template": "{{ .System }}\n{{ .Prompt }}",
        "details": {
            "format": "gguf",
            "family": "llama",
            "parameter_size": "7B",
            "quantization_level": "Q4_0"
        }
    }


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "message": "Mock Ollama Server is running",
        "version": "1.0.0"
    }


@app.get("/api/version")
async def version():
    """Return API version."""
    return {"version": "0.1.0"}


def run_server(host: str = "127.0.0.1", port: int = 11434):
    """Run the mock Ollama server."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
