from google.adk.cli.fast_api import get_fast_api_app
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file
load_dotenv()

app = get_fast_api_app(agents_dir="./src/agents", reload_agents=True, web=True)


def run_server(host="127.0.0.1", port=8000):
    """Run the FastAPI server."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
