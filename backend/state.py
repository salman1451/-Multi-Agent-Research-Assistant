from typing import TypedDict, List

# 💡 Step 1: The "Shared Notepad" (State)
class AgentState(TypedDict):
    query: str               
    subtasks: List[str]      
    current_subtask_index: int  
    search_results: List[dict] 
    summaries: List[str]     
    source_urls: List[str]   
    critique_passed: bool    
    critique_feedback: str   
    final_report: str        
    retry_count: int         
    last_agent: str          
