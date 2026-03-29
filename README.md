# 🧠 Multi-Agent Research Assistant

A powerful, **LangGraph-powered** research system where multiple specialized AI agents collaborate autonomously to research any topic and produce a structured, cited report. 

![Project Overview](https://img.shields.io/badge/LangGraph-Agentic-blue?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Python-FastAPI-Streamlit-green?style=for-the-badge)

## 🤖 How It Works (Agent Flow)
The system mimics a professional research team through five specialized agents:

1.  **Orchestrator Agent**: The "manager." Breaks down your query into focused sub-tasks and assigns them.
2.  **Search Agent**: Uses the **Tavily Search API** to fetch real-time web results. It uses LLM-driven query optimization to find the best data.
3.  **Summarizer Agent**: Compresses raw search results into clean, factual summaries, removing noise and fluff.
4.  **Critique Agent**: The "Quality Guard." Reviews summaries for gaps or missing angles. It can send tasks back for another search loop if the quality isn't high enough (**Self-Correction**).
5.  **Synthesizer Agent**: The "Lead Author." Combines all approved summaries and source URLs into a professional, structured Markdown report.

---

## 🛠️ Tech Stack
- **Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph) (State Management & Agent Flow)
- **Framework**: [LangChain](https://python.langchain.com/)
- **LLM**: OpenAI GPT-4o & GPT-4o-mini (Optimized for speed/quality balance)
- **Search**: [Tavily AI](https://tavily.com/)
- **Backend API**: FastAPI
- **Frontend UI**: Streamlit

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/salman1451/-Multi-Agent-Research-Assistant.git
cd -Multi-Agent-Research-Assistant
```

### 2. Set Up Environment
Create a `.env` file in the root directory and add your API keys:
```text
OPENAI_API_KEY=sk-your-key-here
TAVILY_API_KEY=tvly-your-key-here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
You will need two terminals:

**Terminal 1 (Backend API):**
```bash
python -m backend.main
```

**Terminal 2 (Frontend UI):**
```bash
streamlit run frontend/app.py
```

---

## 🏗️ Project Structure
```text
.
├── backend/
│   ├── main.py        # FastAPI Server
│   ├── graph.py       # LangGraph Workflow logic
│   ├── agents.py      # Individual Agent logic
│   ├── state.py       # Shared Notepad (Graph State)
│   ├── tools.py       # Tavily Search tool
│   ├── prompts.py     # System instructions for LLM
│   └── config.py      # Settings and API keys
├── frontend/
│   └── app.py         # Streamlit User Interface
├── requirements.txt   # Project Dependencies
└── README.md          # You are here!
```

---

## 🛡️ License
Distrubuted under the MIT License. See `LICENSE` for more information.

---
**Created by [salman1451](https://github.com/salman1451)**
