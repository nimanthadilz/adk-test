from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.mark.asyncio
async def test_with_single_test_file():
    """Test the agent's basic ability via a session file."""
    await AgentEvaluator.evaluate(
        agent_module="src.agents.orchestrator_agent",
        eval_dataset_file_path_or_dir="./src/tests/agents/orchestrator_agent/evalset56f9a2.evalset.json",
    )