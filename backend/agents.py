import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from backend.state import AgentState
from backend.prompts import (
    ORCHESTRATOR_PROMPT, 
    SEARCH_AGENT_PROMPT, 
    SUMMARIZER_AGENT_PROMPT, 
    CRITIQUE_AGENT_PROMPT, 
    SYNTHESIZER_AGENT_PROMPT
)

from backend.config import Config, logger
from backend.tools import search_tool


# Initialize the LLMs
# Heavy: For planning and final synthesis
llm = ChatOpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)

# Fast: For intermediate steps (Searching, Summarizing, Critiquing)
fast_llm = ChatOpenAI(model="gpt-4o-mini", api_key=Config.OPENAI_API_KEY)

# --- Step 4: The Controller Manager (Orchestrator) ---
def orchestrator_agent(state: AgentState):
    """Takes the main query and breaks it into 3 subtasks."""
    query = state['query']
    logger.info(f"Orchestrator is processing query: {query}")

    messages = [
        SystemMessage(content=ORCHESTRATOR_PROMPT),
        HumanMessage(content=f"Please break down this research topic: {query}")
    ]

    response = llm.invoke(messages)

    try:
        # The AI returns a list, e.g., ["Task 1", "Task 2", "Task 3"]
        subtasks = json.loads(response.content)
    except Exception as e:
        logger.error(f"Failed to parse research subtasks: {e}")
        subtasks = [query]

    # We save the list in the 'subtasks' folder of our notepad!
    return {
        "subtasks": subtasks,
        "current_subtask_index": 0, # Start at the first one
        "last_agent": "Orchestrator"
    }


# --- Step 5: The Researcher (Search Agent) ---
def search_agent(state: AgentState):
    """
    Refines the research task into a search query and fetches results.
    """
    subtasks = state['subtasks']
    index = state['current_subtask_index']
    
    # 💡 Safety Check: Exit if index is out of bounds
    if index >= len(subtasks):
        logger.warning(f"Search Agent error: Index {index} is out of bounds for subtasks (len: {len(subtasks)}).")
        # In a real graph, we'd route to synthesizer, but we'll return early to prevent crash.
        return {"last_agent": "Search", "critique_passed": True} # Force pass to exit

    current_task = subtasks[index]
    feedback = state.get('critique_feedback', "")

    logger.info(f"Search Agent optimizing query for task: {current_task}")

    # 1. Optimize the search query using the LLM
    context = f"Task: {current_task}"
    if feedback and feedback != "PASS":
        context += f"\nCritique Feedback: {feedback}"

    messages = [
        SystemMessage(content=SEARCH_AGENT_PROMPT),
        HumanMessage(content=context)
    ]
    
    optimized_query = fast_llm.invoke(messages).content.strip()
    logger.info(f"Optimized Query: {optimized_query}")

    # 2. Use the search tool
    results = search_tool(optimized_query)

    # 3. Collect source URLs for citations
    all_urls = state.get('source_urls', [])
    for item in results:
        url = item.get('url')
        if url and url not in all_urls:
            all_urls.append(url)

    # 4. Return new findings
    return {
        "search_results": results,
        "source_urls": all_urls,
        "last_agent": "Search"
    }


# --- Step 6: The Fact Checker (Summarizer Agent) ---
def summarizer_agent(state: AgentState):
    """
    Takes the raw search results from the Search Agent and 
    compresses them into a clean, factual summary.
    """
    search_results = state['search_results']
    logger.info(f"Summarizer Agent is processing {len(search_results)} search results.")

    # 1. Format the search results into a string for the LLM
    context = ""
    for i, res in enumerate(search_results):
        context += f"\nSource {i+1} ({res['url']}):\n{res['content']}\n"

    # 2. Call the LLM with the Summarizer Prompt
    messages = [
        SystemMessage(content=SUMMARIZER_AGENT_PROMPT),
        HumanMessage(content=f"Please summarize these search results:\n{context}")
    ]

    response = fast_llm.invoke(messages)
    summary = response.content

    # 3. Add this summary to our 'summaries' list in the notepad
    all_summaries = state.get('summaries', [])
    all_summaries.append(summary)

    return {
        "summaries": all_summaries,
        "last_agent": "Summarizer"
    }


# --- Step 7: The Quality Guard (Critique Agent) ---
def critique_agent(state: AgentState):
    """
    Evaluates the last summary against the current sub-task.
    If it's weak, gives feedback. If it's strong, says "PASS".
    """
    subtasks = state['subtasks']
    index = state['current_subtask_index']
    current_task = subtasks[index]
    
    # Get the latest summary we just wrote
    last_summary = state['summaries'][-1]
    
    logger.info(f"Critique Agent is evaluating summary for task: {current_task}")

    messages = [
        SystemMessage(content=CRITIQUE_AGENT_PROMPT),
        HumanMessage(content=f"Sub-task: {current_task}\n\nSummary: {last_summary}")
    ]

    response = fast_llm.invoke(messages)
    feedback = response.content.strip()
    current_retries = state.get('retry_count', 0)

    # 💡 Logic:
    # 1. If it passes OR we've reached max retries -> Move to next task
    # 2. Otherwise -> Increment retry count and try again
    
    if "PASS" in feedback.upper():
        logger.info(f"Task {index + 1} PASSED critique.")
        return {
            "critique_passed": True,
            "critique_feedback": "PASS",
            "retry_count": 0, # Reset for next task
            "current_subtask_index": index + 1,
            "last_agent": "Critique"
        }
    elif current_retries >= Config.MAX_RETRIES:
        logger.warning(f"Task {index + 1} hit max retries. Moving on anyway.")
        return {
            "critique_passed": False,
            "critique_feedback": f"Max retries reached. Progressing despite gaps. Last feedback: {feedback}",
            "retry_count": 0, # Reset for next task
            "current_subtask_index": index + 1, 
            "last_agent": "Critique"
        }
    else:
        logger.info(f"Critique failed (Try {current_retries + 1}). Feedback: {feedback}")
        return {
            "critique_passed": False,
            "critique_feedback": feedback,
            "retry_count": current_retries + 1,
            # Index stays the same (retry current task)
            "last_agent": "Critique"
        }


# --- Step 8: The Lead Author (Synthesizer Agent) ---
def synthesizer_agent(state: AgentState):
    """
    Combines all summaries and source URLs into one final Markdown report.
    """
    all_summaries = state['summaries']
    all_urls = state.get('source_urls', [])
    
    logger.info("Synthesizer Agent is writing the final report.")

    # Format summaries for the LLM
    context = "\n\n".join(all_summaries)
    urls_list = "\n".join(all_urls)

    messages = [
        SystemMessage(content=SYNTHESIZER_AGENT_PROMPT),
        HumanMessage(content=f"Summaries:\n{context}\n\nSources:\n{urls_list}")
    ]

    response = llm.invoke(messages)
    
    return {
        "final_report": response.content,
        "last_agent": "Synthesizer"
    }

