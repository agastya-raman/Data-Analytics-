import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("outputs/charts", exist_ok=True)

def plot_distribution(file_path, column, save_name):
    df = pd.read_csv(file_path)
    fig, ax = plt.subplots(figsize=(8,4))
    df[column].dropna().hist(bins=30, ax=ax, color="#185FA5", edgecolor="white", alpha=0.8)
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column); ax.set_ylabel("Count")
    path = f"outputs/charts/{save_name}.png"
    plt.tight_layout(); plt.savefig(path, dpi=120); plt.close()
    return path

def plot_correlation_heatmap(file_path, save_name):
    df = pd.read_csv(file_path)
    fig, ax = plt.subplots(figsize=(10,8))
    sns.heatmap(df.select_dtypes(include=["int64","float64"]).corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation matrix")
    path = f"outputs/charts/{save_name}.png"
    plt.tight_layout(); plt.savefig(path, dpi=120); plt.close()
    return path

def plot_bar(file_path, column, save_name, top_n=10):
    df = pd.read_csv(file_path)
    fig, ax = plt.subplots(figsize=(8,4))
    df[column].value_counts().head(top_n).plot(kind="bar", ax=ax, color="#0F6E56", edgecolor="white")
    ax.set_title(f"Top {top_n} values — {column}")
    plt.xticks(rotation=45, ha="right")
    path = f"outputs/charts/{save_name}.png"
    plt.tight_layout(); plt.savefig(path, dpi=120); plt.close()
    return path

def plot_boxplot(file_path, x_col, y_col, save_name):
    df = pd.read_csv(file_path)
    fig, ax = plt.subplots(figsize=(8,5))
    df.boxplot(column=y_col, by=x_col, ax=ax)
    ax.set_title(f"{y_col} by {x_col}"); plt.suptitle("")
    path = f"outputs/charts/{save_name}.png"
    plt.tight_layout(); plt.savefig(path, dpi=120); plt.close()
    return path
