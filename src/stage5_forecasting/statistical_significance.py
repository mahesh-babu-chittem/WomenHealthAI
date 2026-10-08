import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import ttest_rel, wilcoxon

from src.stage5_forecasting.config import HORIZON as CONFIG_HORIZON
from src.stage5_forecasting.evaluation_utils import find_prediction_file, prediction_key_frame

RESULTS_DIR = Path("results/stage5_forecasting")


def cohens_d(x, y):
    diff = np.asarray(x) - np.asarray(y)
    std = diff.std(ddof=1)
    if std == 0 or np.isnan(std):
        return 0.0
    return float(diff.mean() / std)


def compare_models(tft_file, baseline_file, comparison_name, horizon):
    tft_df = prediction_key_frame(pd.read_csv(tft_file), horizon)
    baseline_df = prediction_key_frame(pd.read_csv(baseline_file), horizon)

    key = ["participant_id", "target_day", "forecast_horizon"]
    tft_df = tft_df.rename(columns={
        "_actual": "tft_actual",
        "_predicted": "tft_predicted",
        "_error": "tft_error",
    })
    baseline_df = baseline_df.rename(columns={
        "_actual": "baseline_actual",
        "_predicted": "baseline_predicted",
        "_error": "baseline_error",
    })

    matched = pd.merge(
        baseline_df,
        tft_df,
        on=key,
        how="inner",
        validate="one_to_one",
    )

    if matched.empty:
        raise ValueError(
            f"No matched participant/date targets for {comparison_name}. "
            "Paired tests cannot be performed."
        )

    # Require actual RHRS to agree on the matched key. This catches accidental
    # mismatched/shifted files before statistical testing.
    actual_diff = np.abs(matched["baseline_actual"] - matched["tft_actual"])
    if not np.allclose(actual_diff.to_numpy(), 0.0, atol=1e-8, rtol=0.0):
        raise ValueError(f"Actual RHRS values disagree for matched targets in {comparison_name}.")

    baseline_error = matched["baseline_error"].to_numpy(dtype=float)
    tft_error = matched["tft_error"].to_numpy(dtype=float)

    t_stat, p_ttest = ttest_rel(baseline_error, tft_error)
    try:
        w_stat, p_wilcoxon = wilcoxon(baseline_error, tft_error)
    except Exception:
        w_stat = np.nan
        p_wilcoxon = np.nan

    return {
        "Comparison": comparison_name,
        "Baseline_Mean_Error": float(baseline_error.mean()),
        "TFT_Mean_Error": float(tft_error.mean()),
        "Mean_Improvement": float(baseline_error.mean() - tft_error.mean()),
        "Paired_t_stat": float(t_stat),
        "Paired_t_pvalue": float(p_ttest),
        "Wilcoxon_stat": float(w_stat) if not pd.isna(w_stat) else np.nan,
        "Wilcoxon_pvalue": float(p_wilcoxon) if not pd.isna(p_wilcoxon) else np.nan,
        "Cohens_d": cohens_d(baseline_error, tft_error),
    }


# The original workflow writes generic filenames. If horizon-prefixed snapshots
# exist, they are preferred so H7 and H14 can be compared in one run.
model_names = [
    "linear_regression",
    "random_forest",
    "xgboost",
    "lstm",
    "gru",
    "bilstm",
    "transformer",
]

results = []
for horizon in [7, 14]:
    tft_file = find_prediction_file(RESULTS_DIR, horizon, "tft")
    if tft_file is None:
        if CONFIG_HORIZON == horizon:
            raise FileNotFoundError(
                f"TFT prediction file for H{horizon} not found. Run tft_model.py first."
            )
        continue

    for model_name in model_names:
        baseline_file = find_prediction_file(RESULTS_DIR, horizon, model_name)
        if baseline_file is None:
            continue

        comparison_name = f"H{horizon} TFT vs {model_name}"
        results.append(
            compare_models(tft_file, baseline_file, comparison_name, horizon)
        )

if not results:
    raise RuntimeError(
        "No statistical comparisons were generated. Ensure the canonical prediction CSVs "
        "for the requested horizon(s) exist."
    )

results_df = pd.DataFrame(results).sort_values(by="Paired_t_pvalue")
results_df.to_csv(RESULTS_DIR / "Table_18_Statistical_Significance.csv", index=False)

significant_df = results_df[results_df["Paired_t_pvalue"] < 0.05]
significant_df.to_csv(RESULTS_DIR / "Table_19_Significant_Comparisons.csv", index=False)

print("\n========================")
print("STATISTICAL SIGNIFICANCE")
print("========================\n")
print(results_df)
print("\nMatched-pair counts:")
for horizon in [7, 14]:
    tft_file = find_prediction_file(RESULTS_DIR, horizon, "tft")
    if tft_file is not None:
        try:
            print(f"H{horizon}: {len(prediction_key_frame(pd.read_csv(tft_file), horizon))} TFT targets")
        except Exception:
            pass
print("\nSaved:")
print(RESULTS_DIR / "Table_18_Statistical_Significance.csv")
print(RESULTS_DIR / "Table_19_Significant_Comparisons.csv")
