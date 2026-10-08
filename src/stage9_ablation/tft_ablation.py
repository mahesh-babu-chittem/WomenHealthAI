import argparse
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

from ablation_config import ABLATIONS, BASE_FEATURES, HORIZONS, RESULT_FILES, get_selected_features, get_weights

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "processed" / "rhrs_dataset.csv"
RESULTS_DIR = ROOT / "results" / "stage9_ablation"
EXPECTED_ORDER = list(ABLATIONS)


class SequenceDataset(Dataset):
    def __init__(self, x, y):
        self.x = torch.tensor(x, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index]


class WomenHealthAITFT(nn.Module):
    def __init__(self, input_size, horizon, temporal_attention=True, adaptive_variable_selection=True, hidden_size=32, heads=4):
        super().__init__()
        self.temporal_attention = temporal_attention
        self.adaptive_variable_selection = adaptive_variable_selection
        self.variable_gate = nn.Linear(input_size, input_size)
        self.encoder = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.attention = nn.MultiheadAttention(hidden_size, heads, batch_first=True)
        self.norm = nn.LayerNorm(hidden_size)
        self.output = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, horizon),
        )

    def forward(self, x):
        if self.adaptive_variable_selection:
            weights = torch.softmax(self.variable_gate(x), dim=-1)
            x = x * weights
        encoded, _ = self.encoder(x)
        if self.temporal_attention:
            attended, _ = self.attention(encoded, encoded, encoded, need_weights=False)
            encoded = self.norm(encoded + attended)
        return self.output(encoded[:, -1, :])


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def build_rhrs_target(frame, ablation_key):
    weights = get_weights(ablation_key)
    available = [key for key in weights if key in frame.columns]
    total = sum(weights[key] for key in available)
    if total == 0:
        raise ValueError("No RHRS dimensions are available for target construction.")
    return sum(frame[key] * weights[key] for key in available) / total


def make_sequences(frame, feature_names, horizon, encoder_length):
    xs = []
    ys = []
    for participant_id, group in frame.groupby("id"):
        group = group.sort_values("day_in_study").reset_index(drop=True)
        values = group[feature_names].to_numpy(dtype=np.float32)
        target = group["RHRS_TARGET"].to_numpy(dtype=np.float32)
        for end in range(encoder_length, len(group) - horizon + 1):
            xs.append(values[end - encoder_length:end])
            ys.append(target[end:end + horizon])
    if not xs:
        raise ValueError("No sequences could be created from the supplied dataset.")
    return np.asarray(xs), np.asarray(ys)


def standardize(train_x, other_x):
    mean = train_x.reshape(-1, train_x.shape[-1]).mean(axis=0)
    std = train_x.reshape(-1, train_x.shape[-1]).std(axis=0)
    std[std < 1e-8] = 1.0
    return (train_x - mean) / std, (other_x - mean) / std


def metrics(y_true, y_pred):
    yt = y_true.reshape(-1)
    yp = y_pred.reshape(-1)
    error = yp - yt
    mae = float(np.mean(np.abs(error)))
    rmse = float(np.sqrt(np.mean(error ** 2)))
    ss_res = float(np.sum(error ** 2))
    ss_tot = float(np.sum((yt - np.mean(yt)) ** 2))
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0
    r = float(np.corrcoef(yt, yp)[0, 1]) if np.std(yt) > 0 and np.std(yp) > 0 else 0.0
    return {"MAE": mae, "RMSE": rmse, "R2": r2, "r": r}


def train_one(frame, ablation_key, horizon, seed, epochs, batch_size, learning_rate):
    selected = get_selected_features(ablation_key)
    frame = frame.copy()
    frame["RHRS_TARGET"] = build_rhrs_target(frame, ablation_key)
    frame = frame.dropna(subset=selected + ["RHRS_TARGET"])
    participants = sorted(frame["id"].unique())
    split = max(1, int(len(participants) * 0.8))
    train_ids = set(participants[:split])
    train_frame = frame[frame["id"].isin(train_ids)]
    test_frame = frame[~frame["id"].isin(train_ids)]
    if test_frame.empty:
        raise ValueError("Participant-level test split is empty.")
    train_x, train_y = make_sequences(train_frame, selected, horizon, 14)
    test_x, test_y = make_sequences(test_frame, selected, horizon, 14)
    train_x, test_x = standardize(train_x, test_x)
    train_ds = SequenceDataset(train_x, train_y)
    test_ds = SequenceDataset(test_x, test_y)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    seed_everything(seed)
    model = WomenHealthAITFT(
        len(selected),
        horizon,
        temporal_attention=ABLATIONS[ablation_key]["temporal_attention"],
        adaptive_variable_selection=ABLATIONS[ablation_key]["adaptive_variable_selection"],
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()
    model.train()
    for _ in range(epochs):
        for xb, yb in train_loader:
            optimizer.zero_grad()
            prediction = model(xb)
            loss = loss_fn(prediction, yb)
            loss.backward()
            optimizer.step()
    model.eval()
    predictions = []
    actuals = []
    with torch.no_grad():
        for xb, yb in test_loader:
            predictions.append(model(xb).cpu().numpy())
            actuals.append(yb.cpu().numpy())
    y_pred = np.concatenate(predictions)
    y_true = np.concatenate(actuals)
    return metrics(y_true, y_pred)


def run_experiment(horizon, epochs, batch_size, learning_rate, seed):
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")
    frame = pd.read_csv(DATA_PATH)
    required = {"id", "day_in_study", *BASE_FEATURES}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing dataset columns: {missing}")
    results = []
    for ablation_key in EXPECTED_ORDER:
        result = train_one(frame, ablation_key, horizon, seed, epochs, batch_size, learning_rate)
        results.append({
            "configuration": ABLATIONS[ablation_key]["label"],
            "ablation_type": ABLATIONS[ablation_key].get("type"),
            "target_mode": ABLATIONS[ablation_key].get("target_mode", "full_rhrs"),
            **result,
        })
        print(f"{horizon}-day | {ablation_key} | {result}")
    payload = {
        "experiment": "WomenHealthAI Ablation Study",
        "task": f"{horizon}-day RHRS forecasting",
        "target_definition": "Full RHRS target for input-removal and architectural ablations; equal-weight RHRS only for the weighting ablation.",
        "metrics": {
            "MAE": "lower_is_better",
            "RMSE": "lower_is_better",
            "R2": "higher_is_better",
            "r": "higher_is_better",
        },
        "results": results,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = ROOT / RESULT_FILES[horizon]
    output_path.write_text(json.dumps(payload, indent=2))
    return output_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--horizon", type=int, choices=list(HORIZONS), nargs="+", default=list(HORIZONS))
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    for horizon in args.horizon:
        output = run_experiment(horizon, args.epochs, args.batch_size, args.learning_rate, args.seed)
        print(f"Saved {output}")


if __name__ == "__main__":
    main()
