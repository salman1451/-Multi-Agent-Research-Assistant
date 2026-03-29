from tavily import TavilyClient
from backend.config import Config, logger

# 💡 Step 4: The Researcher's Tool (Tavily)
# This file is responsible for talking to the internet.
# We use the Tavily Search API because it is optimized for AI agents.

# Initialize the Tavily client with your API key
tavily = None
if Config.TAVILY_API_KEY:
    tavily = TavilyClient(api_key=Config.TAVILY_API_KEY)
else:
    logger.warning("⚠️ TAVILY_API_KEY not found. Search will not work.")

def search_tool(query: str):
    """
    Given a query string, this function searches the web 
    and returns a list of results (titles, URLs, and snippets).
    """
    if not tavily:
        return [{"url": "N/A", "content": "Search is disabled: No API Key."}]

    logger.info(f"Tavily is searching for: {query}")
    
    # We call Tavily with 'search_depth=advanced' for better quality
    response = tavily.search(query=query, search_depth="advanced", max_results=5)
    
    # Return just the results part of the response
    return response.get('results', [])
