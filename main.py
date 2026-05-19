import sys
import os

# LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "langgraph-analytics"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import app

def run_analysis(dataset_path: str):
    print(f"\n{'='*50}\n  LangGraph Analytics Pipeline\n  Dataset: {dataset_path}\n{'='*50}\n")
    initial_state = {
        "dataset_path": dataset_path,
        "cleaned_dataset_path": None,
        "profile_report": None,
        "quality_issues": [],
        "cleaning_log": [],
        "hypotheses": [],
        "findings": [],
        "visualizations": [],
        "current_phase": "profiling",
        "messages": [],
        "errors": [],
        "human_feedback": None,
        "iteration_count": 0,
        "token_count": 0
    }
    print("Running pipeline...\n")
    for step in app.stream(initial_state):
        for node_name, node_output in step.items():
            msgs = node_output.get("messages", [])
            errs = node_output.get("errors", [])
            vizs = node_output.get("visualizations", [])
            phase = node_output.get("current_phase", "")
            print(f"  ✓ {node_name.upper()} (phase→{phase})")
            for m in msgs:
                print(f"    → {m['content'][:150]}")
            for e in errs:
                print(f"    ✗ ERROR: {e['error'][:150]}")
            for v in vizs:
                print(f"    📊 Chart: {v['file_path']}")
            print()

    print("Pipeline complete.")
    print("Report → outputs/reports/report_latest.md")
    print("Charts → outputs/charts/")
    print("Logs   → outputs/logs/\n")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/titanic.csv"
    run_analysis(path)