import json
from pathlib import Path

import pandas as pd

from ablation_config import RESULT_FILES, ABLATIONS

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results" / "stage9_ablation"
EXPECTED_ORDER = [ABLATIONS[key]["label"] for key in ABLATIONS]


def load_result(horizon):
    path = ROOT / RESULT_FILES[horizon]
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text())
    expected_task = f"{horizon}-day RHRS forecasting"
    if data.get("task") != expected_task:
        raise ValueError(f"Unexpected task in {path}")
    labels = [row["configuration"] for row in data.get("results", [])]
    if labels != EXPECTED_ORDER:
        raise ValueError(f"Unexpected configuration set in {path}")
    return data


def main():
    d7 = load_result(7)
    d14 = load_result(14)
    rows = []
    for row7, row14 in zip(d7["results"], d14["results"]):
        rows.append({
            "Configuration": row7["configuration"],
            "7d_MAE": row7["MAE"],
            "7d_RMSE": row7["RMSE"],
            "7d_R2": row7["R2"],
            "7d_r": row7["r"],
            "14d_MAE": row14["MAE"],
            "14d_RMSE": row14["RMSE"],
            "14d_R2": row14["R2"],
            "14d_r": row14["r"],
        })
    df = pd.DataFrame(rows)
    full = df.iloc[0]
    df["7d_RMSE_Delta"] = df["7d_RMSE"] - full["7d_RMSE"]
    df["14d_RMSE_Delta"] = df["14d_RMSE"] - full["14d_RMSE"]
    output_csv = RESULTS_DIR / "ablation_aggregate_results.csv"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(df.to_string(index=False, float_format=lambda value: f"{value:.3f}"))
    print(f"Saved aggregate results to {output_csv}")


if __name__ == "__main__":
    main()
