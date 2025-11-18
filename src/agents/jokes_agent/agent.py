from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

jokes_agent = LlmAgent(
    name="jokes_agent",
    # model="gemini-2.0-flash",
    model=LiteLlm(model="ollama_chat/test_model"),
    description=("An agent that tells jokes related to programming."),
    instruction=(
        """
        You are a humorous programming jokes agent. Your task is to tell funny jokes about programming.
        """
    ),
)
