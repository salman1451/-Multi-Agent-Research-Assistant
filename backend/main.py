from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.graph import graph
from backend.config import logger, validate_env
import uvicorn

# 1. Initialize the API
app = FastAPI(title="Multi-Agent Research Assistant API")

# 2. Define the Request Body
class ResearchRequest(BaseModel):
    query: str

# 3. Define the Research Endpoint
@app.post("/research")
async def run_research(request: ResearchRequest):
    """
    Main entry point for research queries. 
    Invokes the multi-agent graph and returns the final state.
    """
    try:
        logger.info(f"Received research request: {request.query}")
        
        # Initial state for the Graph
        initial_state = {
            "query": request.query,
            "subtasks": [],
            "current_subtask_index": 0,
            "search_results": [],
            "summaries": [],
            "source_urls": [],
            "critique_passed": False,
            "critique_feedback": "",
            "final_report": "",
            "retry_count": 0,
            "last_agent": "User"
        }

        # Invoke the LangGraph (The Brain starts working!)
        final_state = graph.invoke(initial_state)

        # Return the data in the format the Streamlit frontend expects
        return {
            "sub_tasks": final_state.get("subtasks", []),
            "summaries": final_state.get("summaries", []),
            "critique_feedback": final_state.get("critique_feedback", "N/A"),
            "retry_count": final_state.get("retry_count", 0),
            "final_report": final_state.get("final_report", "No report generated.")
        }

    except Exception as e:
        logger.error(f"Research pipeline error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 4. Run the Server
if __name__ == "__main__":
    validate_env()
    uvicorn.run(app, host="0.0.0.0", port=8000)
