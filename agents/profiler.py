import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from state.schema import AnalyticsState
from tools.profiling_tools import profile_dataset

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

def profiler_node(state: AnalyticsState) -> dict:
    try:
        profile = profile_dataset(state.get("cleaned_dataset_path") or state["dataset_path"])
        prompt = f"""You are a data profiler agent.
Dataset profile: {profile}
In 4-5 bullet points summarise the most important observations.
Focus on: high null %, suspicious types, cardinality issues, anything needing attention.
Be specific - mention actual column names and numbers."""
        response = llm.invoke(prompt)
        return {
            "profile_report": profile,
            "current_phase": "profiling",
            "messages": [{"role": "profiler", "content": response.content}]
        }
    except Exception as e:
        return {
            "errors": [{"agent": "profiler", "error": str(e), "phase": "profiling"}],
            "current_phase": "error"
        }