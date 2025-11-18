# Mock Ollama Server

A FastAPI-based mock Ollama server for testing Google ADK agents that use LiteLLM with Ollama models.

## Features

- Implements Ollama API endpoints used by LiteLLM
- Supports both streaming and non-streaming responses
- OpenAI-compatible chat completions endpoint (`/v1/chat/completions`)
- Native Ollama endpoints (`/api/chat`, `/api/tags`, etc.)
- Configurable mock responses
- Lightweight and easy to use

## Installation

Install the required dependencies:

```bash
pip install fastapi uvicorn
```

Or add to your `requirements.txt`:
```
fastapi
uvicorn
```

## Usage

### Starting the Server

Run the server directly:

```bash
python ollama_mock_server/server.py
```

Or run with custom host/port:

```python
from ollama_mock_server.server import run_server

run_server(host="127.0.0.1", port=11434)
```

### Configuration

The server runs on `http://127.0.0.1:11434` by default (Ollama's default port).

To use with your ADK agent, ensure your `.env` file has:

```env
OLLAMA_API_BASE="http://localhost:11434"
```

### Testing

Once the server is running, you can test it with curl:

```bash
# Test chat completion
curl http://localhost:11434/api/chat -d '{
  "model": "test_model",
  "messages": [
    {"role": "user", "content": "Tell me a joke"}
  ]
}'

# List models
curl http://localhost:11434/api/tags

# Health check
curl http://localhost:11434/
```

### Using with Google ADK

Your agent configuration in `agent.py` should work automatically:

```python
from google.adk.models.lite_llm import LiteLlm

model=LiteLlm(model="ollama_chat/test_model")
```

## API Endpoints

- `POST /api/chat` - Native Ollama chat completions
- `POST /v1/chat/completions` - OpenAI-compatible chat completions
- `GET /api/tags` - List available models
- `GET /api/show?name=<model>` - Show model information
- `GET /api/version` - API version
- `GET /` - Health check

## Customizing Mock Responses

Edit the `MOCK_RESPONSES` dictionary in `server.py` to customize responses:

```python
MOCK_RESPONSES = {
    "default": "Your custom default response",
    "joke": "Your custom joke response"
}
```

You can also modify the `get_mock_response()` function to implement more sophisticated response logic based on the input messages.
