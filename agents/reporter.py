import os, json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from state.schema import AnalyticsState

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")


def reporter_node(state: AnalyticsState) -> dict:
    try:
        profile = state.get("profile_report", {}) or {}
        quality_issues = state.get("quality_issues", [])
        cleaning_log = state.get("cleaning_log", [])
        findings = state.get("findings", [])
        visualizations = state.get("visualizations", [])
        messages = state.get("messages", [])
        errors = state.get("errors", [])
        history = "\n".join(f"[{m['role'].upper()}]: {m['content']}" for m in messages)
        prompt = f"""You are a senior data analyst writing an executive report.
Dataset: {profile.get('row_count','?')} rows, {profile.get('column_count','?')} columns.
Agent findings: {history}
Confirmed findings: {json.dumps(findings, indent=2)}
Quality issues: {json.dumps([{'column':i['column'],'issue':i['issue_type'],'severity':i['severity']} for i in quality_issues], indent=2)}
Charts: {chr(10).join(f"- {c['file_path']}: {c['caption']}" for c in visualizations)}
Write a professional markdown report with sections:
# Data Analysis Report
## 1. Executive Summary
## 2. Dataset Overview
## 3. Data Quality
## 4. Key Findings
## 5. Visualizations
## 6. Recommended Next Steps"""
        response = llm.invoke(prompt)
        report = response.content
        os.makedirs("outputs/reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"outputs/reports/report_{timestamp}.md"
        with open(report_path, "w") as f: f.write(report)
        with open("outputs/reports/report_latest.md", "w") as f: f.write(report)
        os.makedirs("outputs/logs", exist_ok=True)
        with open(f"outputs/logs/run_{timestamp}.json", "w") as f:
            json.dump({"timestamp":timestamp,"dataset":state.get("dataset_path"),"quality_issues":quality_issues,"cleaning_log":cleaning_log,"findings":findings,"visualizations":visualizations,"errors":errors}, f, indent=2, default=str)
        return {"current_phase": "done", "messages": [{"role":"reporter","content":f"Report saved to {report_path}"}]}
    except Exception as e:
        return {"errors": [{"agent":"reporter","error":str(e),"phase":"reporting"}], "current_phase":"done"}
