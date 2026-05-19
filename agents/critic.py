import os, json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from state.schema import AnalyticsState

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

def critic_node(state: AnalyticsState) -> dict:
    try:
        findings = state.get("findings", [])
        hypotheses = state.get("hypotheses", [])
        profile = state.get("profile_report", {})

        if not findings:
            return {
                "current_phase": "visualization",
                "messages": [{"role": "critic", "content": "No findings to critique. Moving to visualization."}]
            }

        prompt = f"""You are a critical data science reviewer.
Review these EDA findings and rate their quality.

Dataset has {profile.get('row_count','?')} rows and {profile.get('column_count','?')} columns.

Findings to review:
{json.dumps(findings, indent=2)}

Hypotheses tested:
{json.dumps(hypotheses, indent=2)}

For each finding evaluate:
1. Is the claim statistically sound?
2. Is the evidence strong enough?
3. Is the confidence level appropriate?
4. Any concerns or caveats?

Return JSON array with for each finding:
finding_index, claim, quality_score (1-10), is_valid (bool), concerns, recommendation.
Return ONLY valid JSON. No markdown."""

        response = llm.invoke(prompt)
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"): raw = raw[4:]
        reviews = json.loads(raw.strip())

        valid_indices = [r["finding_index"] for r in reviews if r.get("is_valid", True) and r.get("quality_score", 5) >= 5]
        filtered_findings = [findings[i] for i in valid_indices if i < len(findings)]

        summary = f"Reviewed {len(findings)} findings. {len(filtered_findings)} passed quality check."
        print(f"    [CRITIC] {summary}")

        return {
            "findings": filtered_findings,
            "current_phase": "visualization",
            "messages": [{"role": "critic", "content": summary}]
        }

    except Exception as e:
        return {
            "errors": [{"agent": "critic", "error": str(e), "phase": "critic"}],
            "current_phase": "visualization"
        }
