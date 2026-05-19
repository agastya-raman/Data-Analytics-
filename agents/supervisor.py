from state.schema import AnalyticsState

MAX_EDA_HYPOTHESES = 8
MAX_TOKEN_BUDGET = 50000

def supervisor_route(state: AnalyticsState) -> str:
    phase = state.get("current_phase", "profiling")
    token_count = state.get("token_count", 0)
    quality_issues = state.get("quality_issues", [])
    iter_count = state.get("iteration_count", 0)

    print(f"    [SUPERVISOR] phase={phase} iter={iter_count} issues={len(quality_issues)}")

    if token_count >= MAX_TOKEN_BUDGET: return "reporter"
    if phase == "error": return "reporter"
    if phase == "profiling": return "quality"
    if phase == "quality":
        return "cleaning" if len(quality_issues) > 0 else "eda"
    if phase == "cleaning": return "eda"
    if phase == "eda":
        return "visualization" if iter_count >= MAX_EDA_HYPOTHESES else "eda"
    if phase == "visualization": return "reporter"
    if phase == "reporting": return "reporter"
    if phase == "done": return "reporter"
    return "reporter"