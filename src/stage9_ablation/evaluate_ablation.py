"""Aggregate Stage 9 metrics while preserving skipped/not-evaluable statuses."""
import json
from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1] if SCRIPT_DIR.parent.name == "src" else SCRIPT_DIR.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "stage9_ablation"
FILES = [RESULTS_DIR / "WomenHealthAI_ablation_results_7day.json",
         RESULTS_DIR / "WomenHealthAI_ablation_results_14day.json"]
COLUMNS = ("horizon", "ablation_key", "configuration", "ablation_type", "target_mode",
           "model", "checkpoint", "status", "test_samples", "MAE", "RMSE", "R2", "r", "reason")

def main():
    records = []
    for path in FILES:
        if not path.exists():
            # Do not fabricate missing horizon rows. Existing outputs remain untouched.
            print(f"Skipping missing result file: {path}")
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for result in payload.get("results", []):
            records.append({key: result.get(key) for key in COLUMNS})
    if not records:
        raise FileNotFoundError("No Stage 9 JSON result files found; run the matching Stage 5 checkpoint evaluation first.")
    df = pd.DataFrame(records, columns=COLUMNS)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output = RESULTS_DIR / "ablation_aggregate_results.csv"
    df.to_csv(output, index=False)
    print(df.to_string(index=False))
    print(f"Saved: {output}")

if __name__ == "__main__":
    main()
