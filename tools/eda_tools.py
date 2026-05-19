import pandas as pd
from scipy import stats

def correlation_matrix(file_path: str) -> dict:
    df = pd.read_csv(file_path)
    numeric_df = df.select_dtypes(include=["int64","float64"])
    if numeric_df.empty:
        return {}
    return numeric_df.corr().round(4).to_dict()

def group_comparison(file_path: str, group_col: str, value_col: str) -> dict:
    df = pd.read_csv(file_path)
    if str(df[value_col].dtype) not in ["int64","float64"]:
        return {"error": f"{value_col} is not numeric"}
    return df.groupby(group_col)[value_col].agg(["mean","count","std"]).round(4).to_dict()

def value_counts(file_path: str, column: str) -> dict:
    df = pd.read_csv(file_path)
    return {
        "counts": df[column].value_counts().to_dict(),
        "percentages": (df[column].value_counts(normalize=True).round(4)*100).to_dict()
    }

def distribution_stats(file_path: str, column: str) -> dict:
    df = pd.read_csv(file_path)
    if str(df[column].dtype) not in ["int64","float64"]:
        return {"error": f"{column} is not numeric"}
    s = df[column].dropna()
    return {
        "column": column,
        "count": len(s),
        "mean": round(float(s.mean()), 4),
        "median": round(float(s.median()), 4),
        "std": round(float(s.std()), 4),
        "min": float(s.min()),
        "max": float(s.max()),
        "skewness": round(float(stats.skew(s)), 4),
        "q25": float(s.quantile(0.25)),
        "q75": float(s.quantile(0.75))
    }
