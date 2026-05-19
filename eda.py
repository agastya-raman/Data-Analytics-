import os, json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from state.schema import AnalyticsState
from tools.eda_tools import correlation_matrix, group_comparison, value_counts, distribution_stats

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")
MAX_HYPOTHESES = 8

def eda_node(state: AnalyticsState) -> dict:
    try:
        dataset = state.get("cleaned_dataset_path") or state["dataset_path"]
        profile = state.get("profile_report", {})
        existing = state.get("findings", [])
        iter_cnt = state.get("iteration_count", 0)
        if iter_cnt >= MAX_HYPOTHESES:
            return {"current_phase": "visualization", "messages": [{"role":"eda","content":"Cap reached."}]}
        existing_claims = [f["claim"] for f in existing]
        prompt_hyp = f"""You are an EDA agent.
Columns: {json.dumps(list(profile.get('columns',{}).keys()))}
Already tested: {json.dumps(existing_claims)}
Generate ONE new hypothesis. Return JSON with: hypothesis, test_type (correlation/group_comparison/distribution/value_counts), columns (list), reasoning.
Return ONLY valid JSON."""
        hyp_resp = llm.invoke(prompt_hyp)
        raw = hyp_resp.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"): raw = raw[4:]
        hypothesis = json.loads(raw.strip())
        test_type = hypothesis.get("test_type")
        columns = hypothesis.get("columns", [])
        test_result = {}
        if test_type == "correlation": test_result = correlation_matrix(dataset)
        elif test_type == "group_comparison" and len(columns)==2: test_result = group_comparison(dataset, columns[0], columns[1])
        elif test_type == "value_counts" and columns: test_result = value_counts(dataset, columns[0])
        elif test_type == "distribution" and columns: test_result = distribution_stats(dataset, columns[0])
        prompt_interp = f"""Hypothesis: {hypothesis['hypothesis']}
Results: {json.dumps(test_result, indent=2, default=str)}
Return JSON: claim, evidence, supported (bool), confidence (high/medium/low), chart_type.
Return ONLY valid JSON."""
        interp_resp = llm.invoke(prompt_interp)
        raw2 = interp_resp.content.strip()
        if raw2.startswith("```"):
            raw2 = raw2.split("```")[1]
            if raw2.startswith("json"): raw2 = raw2[4:]
        interp = json.loads(raw2.strip())
        finding = {"claim": interp["claim"], "evidence": interp["evidence"], "chart_path": None, "confidence": interp["confidence"]}
        if interp["claim"] in existing_claims:
            return {"current_phase": "visualization", "messages": [{"role":"eda","content":"Diminishing returns."}]}
        next_phase = "eda" if iter_cnt + 1 < MAX_HYPOTHESES else "visualization"
        return {
            "hypotheses": [{"hypothesis": hypothesis["hypothesis"], "test_type": test_type, "columns": columns, "supported": interp["supported"], "status": "tested"}],
            "findings": [finding] if interp["supported"] else [],
            "current_phase": next_phase,
            "iteration_count": iter_cnt + 1,
            "messages": [{"role":"eda","content":f"Tested: {hypothesis['hypothesis']} — {'Supported' if interp['supported'] else 'Refuted'}"}]
        }
    except Exception as e:
        return {"errors": [{"agent":"eda","error":str(e),"phase":"eda"}], "current_phase":"visualization"}