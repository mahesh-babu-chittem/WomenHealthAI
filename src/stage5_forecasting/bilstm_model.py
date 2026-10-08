import json
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from src.stage5_forecasting.torch_dataset import RHRSDataset
from src.stage5_forecasting.metrics_regression import compute_all_metrics
from src.stage5_forecasting.config import HORIZON
from src.stage5_forecasting.evaluation_utils import load_canonical_split, save_predictions

RESULTS_DIR = Path("results/stage5_forecasting")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
split = load_canonical_split(HORIZON)
X_train, y_train = split["X_train"], split["y_train"]
X_test, y_test = split["X_test"], split["y_test"]
train_loader = DataLoader(RHRSDataset(X_train, y_train), batch_size=32, shuffle=True)

class BiLSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=23, hidden_size=64, num_layers=1, bidirectional=True, batch_first=True)
        self.fc1 = nn.Linear(128, 32)
        self.fc2 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        _, (hidden, _) = self.lstm(x)
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        x = self.relu(self.fc1(hidden))
        return self.fc2(x)

model = BiLSTMModel().to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(50):
    model.train()
    epoch_loss = 0.0
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        outputs = model(X_batch).squeeze()
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    print(f"Epoch {epoch+1}/50 | Loss: {epoch_loss:.4f}")

model.eval()
with torch.no_grad():
    predictions = model(torch.tensor(X_test, dtype=torch.float32).to(device)).cpu().numpy().flatten()

metrics = compute_all_metrics(y_test, predictions)
metrics["Model"] = "BiLSTM"
metrics["Horizon"] = HORIZON
with open(RESULTS_DIR / "bilstm_results.json", "w") as f:
    json.dump(metrics, f, indent=4)
save_predictions(y_test, predictions, split["meta_test"], RESULTS_DIR / "bilstm_predictions.csv", HORIZON)
print(metrics)
