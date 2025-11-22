import logging
import os
import uuid
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from google.adk.agents.run_config import RunConfig
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.adk.runners import Runner
from google.adk.sessions.base_session_service import GetSessionConfig
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.genai.types import Content, Part
from pydantic import BaseModel

from src.agents.jokes_agent.agent import root_agent as jokes_agent

# Load environment variables from .env file
load_dotenv()

# Enable SQLAlchemy logging to see SQL queries
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiosqlite").setLevel(logging.DEBUG)

APP_NAME = "jokes_agent"

app = FastAPI()

db_path = os.path.join(os.getcwd(), "sessions.db")
session_service = SqliteSessionService(db_path=db_path)
runner = Runner(
    agent=jokes_agent,
    app_name="jokes_app",
    session_service=session_service,
)


class UserQueryRequest(BaseModel):
    user_query: str
    user_id: str
    session_id: Optional[str] = None


class AgentResponse(BaseModel):
    agent_response: str


@app.post("/agent")
async def call_agent(request: UserQueryRequest):
    user_id = request.user_id
    session_id = request.session_id or str(uuid.uuid4())

    # Try to create session, ignore if it already exists
    try:
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
    except AlreadyExistsError:
        pass  # Session already exists, runner will fetch it

    user_content = Content(role="user", parts=[Part(text=request.user_query)])

    final_response_content = "No response"
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content,
        run_config=RunConfig(get_session_config=GetSessionConfig(num_recent_events=2)),
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_content = event.content.parts[0].text or "No response"

    return AgentResponse(agent_response=final_response_content)
