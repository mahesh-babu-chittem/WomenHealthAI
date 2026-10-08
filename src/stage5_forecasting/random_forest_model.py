import json
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from src.stage5_forecasting.metrics_regression import compute_all_metrics
from src.stage5_forecasting.config import HORIZON
from src.stage5_forecasting.evaluation_utils import load_canonical_split, save_predictions

RESULTS_DIR = Path("results/stage5_forecasting")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

split = load_canonical_split(HORIZON)
X_train = split["X_train"].reshape(len(split["X_train"]), -1)
X_test = split["X_test"].reshape(len(split["X_test"]), -1)
y_train = split["y_train"]
y_test = split["y_test"]

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

metrics = compute_all_metrics(y_test, predictions)
metrics["Model"] = "Random Forest"
metrics["Horizon"] = HORIZON

with open(RESULTS_DIR / "random_forest_results.json", "w") as f:
    json.dump(metrics, f, indent=4)

save_predictions(
    y_test,
    predictions,
    split["meta_test"],
    RESULTS_DIR / "random_forest_predictions.csv",
    HORIZON,
)

print("\n========================")
print("RANDOM FOREST RESULTS")
print("========================\n")
for k, v in metrics.items():
    print(f"{k}: {v}")
print(f"\nRows Saved: {len(y_test)}")
