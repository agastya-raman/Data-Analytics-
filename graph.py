import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, END
from state.schema import AnalyticsState
from agents.profiler import profiler_node
from agents.quality import quality_node
from agents.cleaning import cleaning_node
from agents.eda import eda_node
from agents.critic import critic_node
from agents.visualization import visualization_node
from agents.reporter import reporter_node

def supervisor_after_profiler(state):
    phase = state.get("current_phase", "")
    issues = state.get("quality_issues", [])
    print(f"    [SUPERVISOR] phase={phase} iter={state.get('iteration_count',0)} issues={len(issues)}")
    if phase == "error": return "reporter"
    return "quality"

def supervisor_after_quality(state):
    phase = state.get("current_phase", "")
    issues = state.get("quality_issues", [])
    print(f"    [SUPERVISOR] phase={phase} iter={state.get('iteration_count',0)} issues={len(issues)}")
    if phase == "error": return "reporter"
    return "cleaning" if len(issues) > 0 else "eda"

def supervisor_after_cleaning(state):
    return "eda"

def supervisor_after_eda(state):
    phase = state.get("current_phase", "")
    iter_count = state.get("iteration_count", 0)
    print(f"    [SUPERVISOR] phase={phase} iter={iter_count} issues={len(state.get('quality_issues',[]))}")
    if phase == "visualization": return "critic"
    if phase == "error": return "reporter"
    return "eda"

def build_graph():
    graph = StateGraph(AnalyticsState)

    graph.add_node("profiler", profiler_node)
    graph.add_node("quality", quality_node)
    graph.add_node("cleaning", cleaning_node)
    graph.add_node("eda", eda_node)
    graph.add_node("critic", critic_node)
    graph.add_node("visualization", visualization_node)
    graph.add_node("reporter", reporter_node)

    graph.set_entry_point("profiler")

    graph.add_conditional_edges("profiler", supervisor_after_profiler, {
        "quality": "quality",
        "reporter": "reporter"
    })
    graph.add_conditional_edges("quality", supervisor_after_quality, {
        "cleaning": "cleaning",
        "eda": "eda",
        "reporter": "reporter"
    })
    graph.add_conditional_edges("cleaning", supervisor_after_cleaning, {
        "eda": "eda"
    })
    graph.add_conditional_edges("eda", supervisor_after_eda, {
        "eda": "eda",
        "critic": "critic",
        "reporter": "reporter"
    })
    graph.add_edge("critic", "visualization")
    graph.add_edge("visualization", "reporter")
    graph.add_edge("reporter", END)

    return graph.compile()

app = build_graph()