from google.adk.cli.fast_api import get_fast_api_app
from dotenv import load_dotenv
import uvicorn
import os

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/mydatabase"

app = get_fast_api_app(agents_dir="./src/agents", reload_agents=True, web=True, session_service_uri=db_url)


def run_server(host="0.0.0.0", port=8000):
    """Run the FastAPI server."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
