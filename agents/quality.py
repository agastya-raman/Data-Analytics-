import os, json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from state.schema import AnalyticsState

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

def quality_node(state: AnalyticsState) -> dict:
    try:
        profile = state.get("profile_report", {})
        prompt = f"""You are a data quality agent.
Dataset profile: {json.dumps(profile, indent=2)}
Find ALL data quality issues. For each return JSON with:
column, issue_type, severity (high/medium/low), evidence, proposed_fix, status (proposed), requires_hitl (always set this to false)
Return ONLY a valid JSON array. No markdown. No explanation."""
        response = llm.invoke(prompt)
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"): raw = raw[4:]
        issues = json.loads(raw.strip())
        # Force requires_hitl to False for all issues
        for issue in issues:
            issue["requires_hitl"] = False
            issue["status"] = "proposed"
        return {
            "quality_issues": issues,
            "current_phase": "quality",
            "messages": [{"role": "quality", "content": f"Found {len(issues)} issues."}]
        }
    except Exception as e:
        return {
            "errors": [{"agent": "quality", "error": str(e), "phase": "quality"}],
            "current_phase": "error"
        }