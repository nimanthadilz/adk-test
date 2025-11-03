from google.adk.agents import LlmAgent

from ..capital_agent import capital_agent

orchestrator_agent = LlmAgent(
    name="orchestrator_agent",
    model="gemini-2.0-flash",
    description=("An agent to orchestrate tasks among multiple agents"),
    instruction=(
        """
        You are an orchestrator agent that delegates tasks to other agents.
        When a user makes a request, determine which sub-agent is best suited to handle the request
        and forward the request to that agent. If the request is out of scope for all sub-agents,
        respond with "Sorry, I cannot handle that request.".
        """
    ),
    sub_agents=[capital_agent],
)

# Expose as root_agent for ADK CLI
root_agent = orchestrator_agent
