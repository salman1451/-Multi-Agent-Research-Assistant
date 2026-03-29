import asyncio
import os
from dotenv import load_dotenv

# Set up environment
load_dotenv()

# We import our graph and agents
from backend.graph import graph

async def debug_the_handshake():
    """ This script shows exactly HOW the notepad is passed! """
    
    print("\n🧐 DEBUGGING THE STATE FLOW 🧐")
    print("--------------------------------")
    
    # 1. Start with a BLANK notepad
    initial_memory = {
        "query": "How are cars made?",
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
    
    print(f"STEP 0: The notepad is empty. Query: '{initial_memory['query']}'")
    print("--------------------------------")

    # 2. Run the graph step-by-step
    # '.stream()' lets us see what each agent does separately
    async for event in graph.astream(initial_memory):
        # An 'event' looks like this: {"orchestrator": {"subtasks": [...]}}
        for agent_name, update in event.items():
            print(f"👉 AGENT JUST FINISHED: {agent_name.upper()}")
            print(f"👉 WHAT THEY ADDED TO MEMORY: {update}")
            print("--------------------------------")

    print("🏁 THE RACE IS OVER!")
    print("Final Notepad is saved in LangGraph's brain.")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY missing.")
    else:
        asyncio.run(debug_the_handshake())
