"""
Test script for the mock Ollama server.
Run this to verify the server is working correctly.
"""
import requests
import json


def test_health():
    """Test the health check endpoint."""
    print("Testing health endpoint...")
    response = requests.get("http://localhost:11434/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_list_models():
    """Test listing models."""
    print("Testing list models endpoint...")
    response = requests.get("http://localhost:11434/api/tags")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_chat_non_streaming():
    """Test non-streaming chat completion."""
    print("Testing non-streaming chat...")
    payload = {
        "model": "test_model",
        "messages": [
            {"role": "user", "content": "Tell me a programming joke"}
        ],
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_chat_streaming():
    """Test streaming chat completion."""
    print("Testing streaming chat...")
    payload = {
        "model": "test_model",
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "stream": True
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload, stream=True)
    print(f"Status: {response.status_code}")
    print("Streaming response:")
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            if chunk.get("message", {}).get("content"):
                print(chunk["message"]["content"], end="", flush=True)
            if chunk.get("done"):
                print("\n[Done]")
    print()


def test_openai_format():
    """Test OpenAI-compatible endpoint."""
    print("Testing OpenAI-compatible endpoint...")
    payload = {
        "model": "test_model",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello"}
        ],
        "stream": False
    }
    response = requests.post("http://localhost:11434/v1/chat/completions", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Mock Ollama Server Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_health()
        test_list_models()
        test_chat_non_streaming()
        test_chat_streaming()
        test_openai_format()
        
        print("=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the server is running: python ollama_mock_server/server.py")
    except Exception as e:
        print(f"Error: {e}")
