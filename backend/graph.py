from langgraph.graph import StateGraph, END

from backend.state import AgentState
from backend.agents import (
    orchestrator_agent,
    search_agent,
    summarizer_agent,
    critique_agent,
    synthesizer_agent,
)


from backend.config import logger, Config

def router(state: AgentState):
    """
    Conditional edge after critique agent.
    1. If failed AND retries remain -> search (retry)
    2. If finished task (passed or max retries) ->
        - If more tasks -> search (next task)
        - If no more tasks -> synthesizer
    """
    index = state.get("current_subtask_index", 0)
    total_tasks = len(state.get("subtasks", []))
    passed = state.get("critique_passed", False)
    retries = state.get("retry_count", 0)

    # 1. Did we fail and have retries left?
    if not passed and retries > 0:
        logger.info(f"Retrying task {index} (Attempts left).")
        return "search"
    
    # 2. Are we done with the current task? Move forward if we can.
    if index < total_tasks:
        logger.info(f"Moving to next task: {index + 1}/{total_tasks}")
        return "search"
    
    # 3. All tasks complete. Synthesis.
    logger.info("All research tasks completed. Finalizing report.")
    return "synthesizer"


def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)

    # ── Add Nodes ──
    workflow.add_node("orchestrator", orchestrator_agent)
    workflow.add_node("search", search_agent)
    workflow.add_node("summarizer", summarizer_agent)
    workflow.add_node("critique", critique_agent)
    workflow.add_node("synthesizer", synthesizer_agent)

    # ── Entry Point ──
    workflow.set_entry_point("orchestrator")

    # ── Linear Edges ──
    workflow.add_edge("orchestrator", "search")
    workflow.add_edge("search", "summarizer")
    workflow.add_edge("summarizer", "critique")

    # ── Conditional Edge: Critique → Synthesizer or back to Search ──
    workflow.add_conditional_edges(
        "critique",
        router,
        {
            "search": "search",
            "synthesizer": "synthesizer",
        }
    )

    # ── End ──
    workflow.add_edge("synthesizer", END)

    return workflow.compile()


# Compiled graph instance (imported by main.py)
graph = build_graph()