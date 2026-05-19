import os, shutil
from dotenv import load_dotenv
from state.schema import AnalyticsState
from tools.cleaning_tools import drop_duplicates, impute_mean, impute_mode, standardise_text

load_dotenv()

def cleaning_node(state: AnalyticsState) -> dict:
    try:
        issues = state.get("quality_issues", [])
        src = state.get("cleaned_dataset_path") or state["dataset_path"]
        os.makedirs("data/processed", exist_ok=True)
        working = "data/processed/cleaned.csv"

        # Always fresh copy
        shutil.copy(src, working)

        import pandas as pd
        log = []

        for issue in issues:
            col = issue.get("column", "")
            issue_type = issue.get("issue_type", "").lower().strip()
            result = None

            try:
                df = pd.read_csv(working)

                # Skip if column doesn't exist
                if col not in df.columns and issue_type != "duplicate_rows":
                    continue

                # Match any null/missing related issue type
                null_keywords = ["null", "missing", "nan", "empty", "incomplete"]
                dup_keywords = ["duplicate", "dup"]
                text_keywords = ["categorical", "whitespace", "inconsistent", "text", "format"]

                if any(k in issue_type for k in dup_keywords):
                    result = drop_duplicates(working, working)

                elif any(k in issue_type for k in null_keywords):
                    dtype = str(df[col].dtype)
                    if dtype in ["int64", "float64"]:
                        result = impute_mean(working, working, col)
                    else:
                        result = impute_mode(working, working, col)

                elif any(k in issue_type for k in text_keywords):
                    result = standardise_text(working, working, col)

                else:
                    # Try to fix based on column dtype anyway
                    dtype = str(df[col].dtype) if col in df.columns else ""
                    if dtype in ["int64", "float64"] and df[col].isnull().sum() > 0:
                        result = impute_mean(working, working, col)
                    elif dtype == "object" and df[col].isnull().sum() > 0:
                        result = impute_mode(working, working, col)

                if result:
                    log.append({
                        "issue_type": issue_type,
                        "column": col,
                        "action": result,
                        "status": "applied"
                    })

            except Exception as col_err:
                log.append({
                    "issue_type": issue_type,
                    "column": col,
                    "status": "failed",
                    "error": str(col_err)
                })

        return {
            "cleaned_dataset_path": working,
            "cleaning_log": log,
            "current_phase": "eda",
            "messages": [{"role": "cleaning", "content": f"Applied {len(log)} cleaning actions."}]
        }

    except Exception as e:
        return {
            "errors": [{"agent": "cleaning", "error": str(e), "phase": "cleaning"}],
            "current_phase": "eda"
        }