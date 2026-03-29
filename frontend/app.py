import streamlit as st
import requests
import os

# 💡 Use the Render backend URL if deployed, otherwise fallback to localhost
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_URL = f"{BACKEND_URL}/research"

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("Multi-Agent Research Assistant")
st.caption("Powered by LangGraph • LangChain • Tavily • GPT-4o")
st.divider()

query = st.text_input(
    "Enter your research topic:",
    placeholder="e.g. What is the current state of quantum computing?"
)

run = st.button(" Research", type="primary", disabled=not query.strip())

if run and query.strip():

    with st.status("🤖 Running multi-agent research pipeline...", expanded=True) as status:

        st.write(" Orchestrator breaking down your query into sub-tasks...")
        st.write(" Search Agent finding relevant information...")
        st.write(" Summarizer Agent extracting key findings...")
        st.write(" Critique Agent evaluating research quality...")
        st.write(" Synthesizer Agent writing final report...")

        try:
            response = requests.post(API_URL, json={"query": query}, timeout=300)
            response.raise_for_status()
            data = response.json()
            status.update(label=" Research complete!", state="complete", expanded=False)

        except requests.exceptions.Timeout:
            status.update(label=" Request timed out", state="error")
            st.error("The research took too long. Try a more specific query.")
            st.stop()

        except requests.exceptions.RequestException as e:
            status.update(label=" Error", state="error")
            st.error(f"Failed to connect to backend: {e}")
            st.stop()

    # ── Results Layout ──
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Sub-Tasks")
        for i, task in enumerate(data.get("sub_tasks", []), 1):
            st.markdown(f"**{i}.** {task}")

        st.divider()

        st.subheader("Critique Feedback")
        feedback = data.get("critique_feedback", "N/A")
        retries = data.get("retry_count", 0)
        st.info(feedback)
        st.caption(f"Retry loops used: {retries}")

    with col2:
        st.subheader(" Final Report")
        st.markdown(data.get("final_report", "No report generated."))

    st.divider()

    with st.expander(" View Raw Summaries"):
        for summary in data.get("summaries", []):
            st.markdown(summary)
            st.divider()