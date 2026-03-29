import asyncio
import os
from dotenv import load_dotenv

# Set up environment
load_dotenv()

# We import the graph we just built
from backend.graph import graph

async def test_communication():
    print("Testing Communication Handshake (Graph)...")
    
    initial_state = {
        "query": "The future of space travel",
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
    
    # Run the graph!!
    # .ainvoke() starts the relay race
    print("🚀 Starting the Relay Race...")
    final_state = await graph.ainvoke(initial_state)
    
    print("\n--- Final Notepad State ---")
    print(f"1. Orchestrator created: {final_state['subtasks']}")
    print(f"2. Search Agent found info for: {final_state['subtasks'][0]}")
    print(f"3. Memory now contains {len(final_state['search_results'])} search results.")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        print("❌ Error: API Keys missing in .env")
    else:
        # Run the async test
        asyncio.run(test_communication())
