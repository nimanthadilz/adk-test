from fastapi import FastAPI
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.cli.fast_api import get_fast_api_app
from google.genai.types import Content, Part
from google.adk.sessions import DatabaseSessionService
from src.agents.jokes_agent.agent import root_agent as jokes_agent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

APP_NAME = "jokes_app"
USER_ID = "user_123"
SESSION_ID = "session_123"

# app = FastAPI(app_name="jokes_app", title="Jokes API", version="1.0.0")
app = get_fast_api_app(agents_dir="./agents", reload_agents=True, web=True)

session_service = DatabaseSessionService(db_url="sqlite:///./sessions.db")
runner = Runner(
    agent=jokes_agent,
    app_name="jokes_app",
    session_service=session_service,
)


class UserQueryRequest(BaseModel):
    user_query: str


class AgentResponse(BaseModel):
    agent_response: str


@app.post("/agent")
async def call_agent(request: UserQueryRequest):
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )

    user_content = Content(role="user", parts=[Part(text=request.user_query)])

    final_response_content = "No response"
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=user_content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_content = event.content.parts[0].text or "No response"

    return AgentResponse(agent_response=final_response_content)
