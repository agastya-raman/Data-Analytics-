from typing import TypedDict, Annotated, List, Optional
import operator

class QualityIssue(TypedDict):
    column: str
    issue_type: str
    severity: str
    evidence: str
    proposed_fix: str
    status: str
    requires_hitl: bool

class Finding(TypedDict):
    claim: str
    evidence: str
    chart_path: Optional[str]
    confidence: str

class AnalyticsState(TypedDict):
    dataset_path: str
    cleaned_dataset_path: Optional[str]
    profile_report: Optional[dict]
    quality_issues: Annotated[List[QualityIssue], operator.add]
    cleaning_log: Annotated[List[dict], operator.add]
    hypotheses: Annotated[List[dict], operator.add]
    findings: Annotated[List[Finding], operator.add]
    visualizations: Annotated[List[dict], operator.add]
    current_phase: str
    messages: Annotated[List[dict], operator.add]
    errors: Annotated[List[dict], operator.add]
    human_feedback: Optional[str]
    iteration_count: int
    token_count: int