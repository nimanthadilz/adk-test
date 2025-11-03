from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext, ReadonlyContext
from google.adk.utils import instructions_utils

capital_agent = LlmAgent(
    name="capital_agent",
    model="gemini-2.0-flash",
    description=("Agent to provide information about capital cities"),
    instruction=(
        """
        You are an agent that provides information about capital cities around the world.
        When user asks about a country's capital, respond with the name of the capital city and a fun fact about it.
        If the country is not recognized, respond with saying "Sorry, I don't know about that country.".
        When providing your answer follow the format:
            "The capital of [country] is <b>[capital city]</b>. 

            <b>Fun fact</b>: [fun fact about the capital city].
            "
    """
    ),
    # before_agent_callback=before_agent_callback,
)
