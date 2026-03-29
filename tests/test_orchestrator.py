import asyncio
import os
from dotenv import load_dotenv

# Set up environment
load_dotenv()

from backend.agents import orchestrator_agent

def test_orchestrator():
    print("Testing Controller Manager (Orchestrator)...")
    
    # Create a mock state
    initial_state = {
        "query": "The future of autonomous electric vehicles",
        "subtasks": [],
        "summaries": [],
        "search_results": [],
        "source_urls": [],
        "critique_passed": False,
        "retry_count": 0,
        "current_subtask_index": 0,
        "final_report": "",
        "last_agent": ""
    }
    
    # Run the agent directly
    result = orchestrator_agent(initial_state)
    
    print("\n--- Result ---")
    print(f"Subtasks created: {result['subtasks']}")
    print(f"Last agent: {result['last_agent']}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env file.")
    else:
        test_orchestrator()
