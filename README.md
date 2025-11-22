# Session Event Limiting Demo

Demonstrates `GetSessionConfig.num_recent_events` functionality with SQLite session store.

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run server
uvicorn main:app --reload
```

## Test

```bash
# Send a message (creates new session)
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Tell me a joke", "user_id": "user123", "session_id": "test-session"}'
```

You should see a DEBUG log indicating only the most recent 2 events are fetched from the session.
```bash
2025-11-22 15:58:28,137 - aiosqlite - DEBUG - operation functools.partial(<bound method Connection._execute_fetchall of <Connection(Thread-14, started 28344)>>, 'SELECT event_data FROM events WHERE app_name=? AND user_id=? AND session_id=? ORDER BY timestamp DESC LIMIT ?', ['jokes_agent', 'uer123', 'test-session', 2]) completed
```

## Configuration

In `main.py`, adjust the event limit:

```python
run_config=RunConfig(get_session_config=GetSessionConfig(num_recent_events=2))
```
