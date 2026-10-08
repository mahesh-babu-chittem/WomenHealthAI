import json
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression
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

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

metrics = compute_all_metrics(y_test, predictions)
metrics["Model"] = "Linear Regression"
metrics["Horizon"] = HORIZON

with open(RESULTS_DIR / "linear_regression_results.json", "w") as f:
    json.dump(metrics, f, indent=4)

# Existing filename is unchanged; canonical keys are appended after the original prediction columns.
save_predictions(
    y_test,
    predictions,
    split["meta_test"],
    RESULTS_DIR / "linear_regression_predictions.csv",
    HORIZON,
)

print("\n===================")
print("LINEAR REGRESSION")
print("===================\n")
for k, v in metrics.items():
    print(f"{k}: {v}")
