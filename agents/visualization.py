import os, json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from state.schema import AnalyticsState
from tools.plot_tools import plot_distribution, plot_correlation_heatmap, plot_bar, plot_boxplot

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

def visualization_node(state: AnalyticsState) -> dict:
    try:
        dataset = state.get("cleaned_dataset_path") or state["dataset_path"]
        findings = list(state.get("findings", []))
        profile = state.get("profile_report", {})
        charts = []

        os.makedirs("outputs/charts", exist_ok=True)

        # Always generate correlation heatmap
        numeric_cols = [col for col, info in profile.get("columns", {}).items()
                       if info["dtype"] in ["int64", "float64"]]

        if len(numeric_cols) >= 2:
            try:
                path = plot_correlation_heatmap(dataset, "correlation_heatmap")
                charts.append({
                    "chart_type": "heatmap",
                    "file_path": path,
                    "caption": "Correlation matrix of numeric columns",
                    "finding_index": None
                })
                print(f"    → Chart saved: {path}")
            except Exception as e:
                print(f"    → Heatmap error: {e}")

        # Generate chart for each finding
        for i, finding in enumerate(findings):
            try:
                prompt = f"""Finding: {finding['claim']}
Columns available: {json.dumps(list(profile.get('columns', {}).keys()))}
Column types: {json.dumps({col: info['dtype'] for col, info in profile.get('columns', {}).items()})}
Return JSON with: chart_type (histogram/bar/boxplot/heatmap/skip), columns (list max 2), caption, reason.
Return ONLY valid JSON. No markdown."""

                resp = llm.invoke(prompt)
                raw = resp.content.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"): raw = raw[4:]
                spec = json.loads(raw.strip())

                if spec["chart_type"] == "skip":
                    continue

                cols = spec.get("columns", [])
                save_name = f"finding_{i}_{spec['chart_type']}"
                path = None

                if spec["chart_type"] == "histogram" and cols:
                    path = plot_distribution(dataset, cols[0], save_name)
                elif spec["chart_type"] == "bar" and cols:
                    path = plot_bar(dataset, cols[0], save_name)
                elif spec["chart_type"] == "boxplot" and len(cols) == 2:
                    path = plot_boxplot(dataset, cols[0], cols[1], save_name)
                elif spec["chart_type"] == "heatmap":
                    path = plot_correlation_heatmap(dataset, save_name)

                if path:
                    charts.append({
                        "chart_type": spec["chart_type"],
                        "file_path": path,
                        "caption": spec["caption"],
                        "finding_index": i
                    })
                    print(f"    → Chart saved: {path}")

            except Exception as chart_err:
                print(f"    → Chart error finding {i}: {chart_err}")
                continue

        return {
            "visualizations": charts,
            "current_phase": "visualization",
            "messages": [{"role": "visualization", "content": f"Generated {len(charts)} charts."}]
        }

    except Exception as e:
        return {
            "errors": [{"agent": "visualization", "error": str(e), "phase": "visualization"}],
            "current_phase": "visualization"
        }