import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from google.adk import Runner
from google.adk.sessions import Session

from agents import project_documentation_team
from config import APP_NAME, DEFAULT_USER_ID, DEFAULT_SESSION_ID_PREFIX, SUB_AGENT_MODEL
from core import call_agent_turn
from core import session_service

load_dotenv()

app = FastAPI()


class ChatAPI:
    def __init__(self):
        self.app_runner: Runner | None = None
        self.session_id_for_this_run: Session | None = None

    async def start_runner(self):
        if not os.getenv("ADK_AGENT_LLM_MODEL"):
            print(
                "⚠️ APP WARNING: ADK_AGENT_LLM_MODEL environment variable is not set. Agents will use defaults from config.py."
            )

        api_key_found = any(
            os.getenv(key)
            for key in [
                "GOOGLE_API_KEY",
                "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY",
            ]
        )
        if not api_key_found:
            print("❌ APP ERROR: No common LLM API Key (e.g., GOOGLE_API_KEY) found in environment variables.")
            print(
                "         Please ensure your .env file is correctly set up and loaded, and contains the required API key."
            )
        else:
            print("✅ LLM API Key seems to be present in environment (ADK/LiteLLM will attempt to use it).")

        if self.app_runner is not None:
            return {"status": "already running"}
        self.session_id_for_this_run = f"{DEFAULT_SESSION_ID_PREFIX}{uuid.uuid4()}"
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=DEFAULT_USER_ID,
            session_id=self.session_id_for_this_run,
        )
        # logs =
        print(f"Session '{self.session_id_for_this_run}' created for app '{APP_NAME}', user '{DEFAULT_USER_ID}'.")

        self.app_runner = Runner(
            agent=project_documentation_team,
            app_name=APP_NAME,
            session_service=session_service,
        )
        print(f"Runner created for root agent '{self.app_runner.agent.name}'.")

        print(f"  (Coordinator Model: {project_documentation_team.model}, Base Sub-Agent Model: {SUB_AGENT_MODEL})")
        print("-" * 70)
        print(f"Starting chat with {project_documentation_team.name}..")
        print("-" * 70)

        return {"status": "started"}

    async def end_runner(self):
        if self.session_id_for_this_run is None:
            return {"status": "not running"}
        self.app_runner = None
        self.session_id_for_this_run = None
        return {"status": "stopped"}

    async def chat_endpoint(self, request: Request):
        if self.app_runner is None:
            return {"error": "Runner not started. Please call /start first."}
        data = await request.json()
        user_query = data["user_query"]
        print(f"User Query: {user_query}")
        result = await call_agent_turn(
            query=user_query,
            runner=self.app_runner,
            user_id=DEFAULT_USER_ID,
            session_id_to_use=self.session_id_for_this_run,
        )
        return {"result": result}


chat_api = ChatAPI()


@app.post("/start")
async def start_runner():
    return await chat_api.start_runner()


@app.post("/end")
async def end_runner():
    return await chat_api.end_runner()


@app.post("/chat")
async def chat_endpoint(request: Request):
    return await chat_api.chat_endpoint(request)
