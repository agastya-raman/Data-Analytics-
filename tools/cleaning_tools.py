import pandas as pd

def drop_duplicates(file_path: str, output_path: str) -> dict:
    df = pd.read_csv(file_path)
    before = len(df)
    df = df.drop_duplicates()
    df.to_csv(output_path, index=False)
    return {"action":"drop_duplicates","rows_before":before,"rows_after":len(df),"rows_removed":before-len(df)}

def impute_mean(file_path: str, output_path: str, column: str) -> dict:
    df = pd.read_csv(file_path)
    null_count = int(df[column].isnull().sum())
    mean_val = round(float(df[column].mean()), 4)
    df[column] = df[column].fillna(mean_val)
    df.to_csv(output_path, index=False)
    return {"action":"impute_mean","column":column,"nulls_filled":null_count,"fill_value":mean_val}

def impute_mode(file_path: str, output_path: str, column: str) -> dict:
    df = pd.read_csv(file_path)
    null_count = int(df[column].isnull().sum())
    mode_val = df[column].mode()[0]
    df[column] = df[column].fillna(mode_val)
    df.to_csv(output_path, index=False)
    return {"action":"impute_mode","column":column,"nulls_filled":null_count,"fill_value":str(mode_val)}

def drop_column(file_path: str, output_path: str, column: str) -> dict:
    df = pd.read_csv(file_path)
    df = df.drop(columns=[column])
    df.to_csv(output_path, index=False)
    return {"action":"drop_column","column_dropped":column}

def standardise_text(file_path: str, output_path: str, column: str) -> dict:
    df = pd.read_csv(file_path)
    df[column] = df[column].astype(str).str.lower().str.strip()
    df.to_csv(output_path, index=False)
    return {"action":"standardise_text","column":column}
