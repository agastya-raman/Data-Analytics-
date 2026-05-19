import pandas as pd


def profile_dataset(file_path: str) -> dict:
    df = pd.read_csv(file_path)
    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": {},
    }
    for col in df.columns:
        s = df[col]
        entry = {
            "dtype": str(s.dtype),
            "null_count": int(s.isnull().sum()),
            "null_pct": round(s.isnull().mean() * 100, 2),
            "cardinality": int(s.nunique()),
            "sample_values": s.dropna().head(5).tolist(),
        }
        if s.dtype in ["int64", "float64"]:
            entry.update(
                {
                    "mean": round(float(s.mean()), 4),
                    "std": round(float(s.std()), 4),
                    "min": float(s.min()),
                    "max": float(s.max()),
                    "q25": float(s.quantile(0.25)),
                    "q75": float(s.quantile(0.75)),
                }
            )
        if s.dtype == "object":
            entry["top_values"] = s.value_counts().head(5).to_dict()
        profile["columns"][col] = entry
    return profile
