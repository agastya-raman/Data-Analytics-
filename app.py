import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
from datetime import datetime

os.makedirs("data/uploads", exist_ok=True)
os.makedirs("outputs/charts", exist_ok=True)
os.makedirs("outputs/reports", exist_ok=True)
os.makedirs("outputs/logs", exist_ok=True)

app = FastAPI(title="LangGraph Analytics")

app.mount("/charts", StaticFiles(directory="outputs/charts"), name="charts")

@app.get("/", response_class=HTMLResponse)
async def home():
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "templates", "index.html"
    )
    if not os.path.exists(template_path):
        return HTMLResponse("<h1 style='color:red'>templates/index.html not found!</h1>")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upload_path = f"data/uploads/dataset_{timestamp}.csv"
        with open(upload_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        from graph import app as graph_app
        initial_state = {
            "dataset_path": upload_path,
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

        steps = []
        for step in graph_app.stream(initial_state):
            for node_name, node_output in step.items():
                steps.append({
                    "agent": node_name.upper(),
                    "phase": node_output.get("current_phase", ""),
                    "messages": [m["content"][:200] for m in node_output.get("messages", [])],
                    "errors": [e["error"][:200] for e in node_output.get("errors", [])],
                    "charts": [v["file_path"] for v in node_output.get("visualizations", [])]
                })

        report = ""
        if os.path.exists("outputs/reports/report_latest.md"):
            with open("outputs/reports/report_latest.md", "r", encoding="utf-8") as f:
                report = f.read()

        charts = []
        if os.path.exists("outputs/charts"):
            charts = [f for f in os.listdir("outputs/charts") if f.endswith(".png")]

        return {
            "success": True,
            "steps": steps,
            "report": report,
            "charts": charts
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "steps": [],
            "report": "",
            "charts": []
        }

@app.get("/report")
async def get_report():
    if os.path.exists("outputs/reports/report_latest.md"):
        return FileResponse(
            "outputs/reports/report_latest.md",
            media_type="text/markdown",
            filename="report.md"
        )
    return {"error": "No report found"}

@app.get("/charts-list")
async def get_charts():
    if os.path.exists("outputs/charts"):
        charts = [f for f in os.listdir("outputs/charts") if f.endswith(".png")]
        return {"charts": charts}
    return {"charts": []}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "charts": len(os.listdir("outputs/charts")) if os.path.exists("outputs/charts") else 0,
        "reports": len(os.listdir("outputs/reports")) if os.path.exists("outputs/reports") else 0
    }