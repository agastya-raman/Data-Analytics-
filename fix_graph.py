content = """import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, END
from state.schema import AnalyticsState
from agents.profiler import profiler_node
from agents.quality import quality_node
from agents.cleaning import cleaning_node
from agents.eda import eda_node
from agents.visualization import visualization_node
from agents.reporter import reporter_node
from agents.supervisor import supervisor_route

def build_graph():
    graph = StateGraph(AnalyticsState)
    graph.add_node("profiler", profiler_node)
    graph.add_node("quality", quality_node)
    graph.add_node("cleaning", cleaning_node)
    graph.add_node("eda", eda_node)
    graph.add_node("visualization", visualization_node)
    graph.add_node("reporter", reporter_node)
    graph.set_entry_point("profiler")
    graph.add_conditional_edges("profiler", supervisor_route, {"quality":"quality","eda":"eda","reporter":"reporter"})
    graph.add_conditional_edges("quality", supervisor_route, {"cleaning":"cleaning","eda":"eda","reporter":"reporter"})
    graph.add_conditional_edges("cleaning", supervisor_route, {"profiler":"profiler","eda":"eda","reporter":"reporter"})
    graph.add_conditional_edges("eda", supervisor_route, {"eda":"eda","visualization":"visualization","reporter":"reporter"})
    graph.add_edge("visualization", "reporter")
    graph.add_edge("reporter", END)
    return graph.compile()

app = build_graph()
"""
with open("graph.py", "w") as f:
    f.write(content)
print("graph.py fixed!")
