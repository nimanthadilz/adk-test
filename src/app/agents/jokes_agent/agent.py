from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="jokes_agent",
    model="gemini-2.0-flash",
    description=("Agent to tell jokes"),
    instruction=("You are an agent that tells jokes."),
    # before_agent_callback=before_agent_callback,
)
