import os
from dotenv import load_dotenv

# Set up environment
load_dotenv()

from backend.agents import search_agent

def test_search():
    print("Testing Researcher (Search Agent)...")
    
    # Create a mock state with a subtask
    mock_state = {
        "query": "The future of autonomous electric vehicles",
        "subtasks": ["technological advancements in autonomous electric vehicles"],
        "current_subtask_index": 0,
        "summaries": [],
        "search_results": [],
        "source_urls": [],
        "critique_passed": False,
        "retry_count": 0,
        "final_report": "",
        "last_agent": ""
    }
    
    # Run the agent directly
    result = search_agent(mock_state)
    
    print("\n--- Result ---")
    print(f"Results found: {len(result['search_results'])}")
    print(f"URLs collected: {result['source_urls'][:2]} ...") # Just show first two
    print(f"Last agent: {result['last_agent']}")

if __name__ == "__main__":
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ Error: TAVILY_API_KEY not found in .env file.")
    else:
        test_search()
