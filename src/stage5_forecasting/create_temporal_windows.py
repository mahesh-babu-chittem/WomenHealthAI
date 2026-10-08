import pandas as pd
import numpy as np
import json
from pathlib import Path

WINDOW_SIZE = 14
FORECAST_HORIZONS = [7, 14]

INPUT_FILE = "data/processed/rhrs_dataset.csv"
OUTPUT_DIR = Path("data/processed/temporal_windows")
RESULTS_DIR = Path("results/stage5_forecasting")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_COLUMNS = [
    "lh", "estrogen", "pdg",
    "mean_rmssd", "mean_lf", "mean_hf",
    "resting_hr",
    "mean_glucose", "std_glucose",
    "sleep_score", "deep_sleep",
    "stress_score",
    "headaches", "cramps", "fatigue", "foodcravings", "bloating",
    "HRS", "PRS", "MRS", "BRS", "SRS", "RHRS"
]


def detect_date_column(columns):
    candidates = [
        "date", "Date", "collection_date", "measurement_date",
        "record_date", "timestamp", "datetime"
    ]
    for c in candidates:
        if c in columns:
            return c
    return None


df = pd.read_csv(INPUT_FILE)
df = df.sort_values(["id", "day_in_study"]).reset_index(drop=True)
DATE_COLUMN = detect_date_column(df.columns)
if DATE_COLUMN:
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")

report = {}

for horizon in FORECAST_HORIZONS:
    X = []
    y = []
    metadata = []
    participant_ids = set()

    for pid in df["id"].dropna().unique():
        participant_df = df[df["id"] == pid].copy().sort_values("day_in_study").reset_index(drop=True)

        if len(participant_df) < WINDOW_SIZE + horizon:
            continue

        for i in range(len(participant_df) - WINDOW_SIZE - horizon + 1):
            encoder = participant_df.iloc[i:i + WINDOW_SIZE]
            target_row = participant_df.iloc[i + WINDOW_SIZE + horizon - 1]

            input_days = pd.to_numeric(encoder["day_in_study"], errors="coerce").to_numpy()
            input_end_day = float(input_days[-1])
            target_day = float(pd.to_numeric(target_row["day_in_study"], errors="coerce"))

            # Require a genuinely contiguous 14-day historical window.
            if not np.all(np.diff(input_days) == 1):
                continue

            # Require the target to be exactly H days after the final observed day.
            if target_day - input_end_day != horizon:
                continue

            if DATE_COLUMN:
                input_dates = encoder[DATE_COLUMN].to_numpy()
                target_date = target_row[DATE_COLUMN]
                if pd.isna(target_date) or pd.isna(input_dates[-1]):
                    continue
                if not np.all(np.diff(input_dates).astype("timedelta64[D]") == np.timedelta64(1, "D")):
                    continue
                if (target_date - input_dates[-1]).days != horizon:
                    continue
                target_date_value = target_date.strftime("%Y-%m-%d")
            else:
                target_date_value = str(int(target_day)) if float(target_day).is_integer() else str(target_day)

            X.append(encoder[FEATURE_COLUMNS].to_numpy(dtype=float))
            y.append(float(target_row["RHRS"]))
            metadata.append({
                "window_index": len(metadata),
                "participant_id": pid,
                "input_start_day": float(input_days[0]),
                "input_end_day": float(input_end_day),
                "target_day": float(target_day),
                "target_date": target_date_value,
                "forecast_horizon": int(horizon),
                "actual_RHRS": float(target_row["RHRS"]),
            })
            participant_ids.add(pid)

    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    metadata_df = pd.DataFrame(metadata)

    if len(X) == 0:
        raise RuntimeError(f"No valid H{horizon} windows were generated.")

    # Strong alignment invariant: every model will use this exact row order.
    assert len(X) == len(y) == len(metadata_df)

    np.save(OUTPUT_DIR / f"X_h{horizon}.npy", X)
    np.save(OUTPUT_DIR / f"y_h{horizon}.npy", y)
    metadata_df.to_csv(OUTPUT_DIR / f"window_metadata_h{horizon}.csv", index=False)

    report[f"horizon_{horizon}"] = {
        "window_size": WINDOW_SIZE,
        "forecast_horizon": horizon,
        "samples": int(len(X)),
        "participants": int(len(participant_ids)),
        "input_shape": list(X.shape),
        "target_shape": list(y.shape),
        "date_column_used": DATE_COLUMN,
        "gap_policy": "Only contiguous 14-day encoder windows and exact H-day target gaps are retained."
    }

with open(RESULTS_DIR / "windows_report.json", "w") as f:
    json.dump(report, f, indent=4)

print(json.dumps(report, indent=4))
