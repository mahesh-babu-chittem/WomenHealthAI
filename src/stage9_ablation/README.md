# Stage 9 — WomenHealthAI Ablation Study

Stage 9 contains the independent WomenHealthAI ablation experiment code and its two horizon-specific result artifacts.

## 1. Directory Structure

```text
project_root/
│
├── stage9_ablation/
│   ├── README.md
│   ├── ablation_config.py
│   ├── tft_ablation.py
│   └── evaluate_ablation.py
│
└── results/
    └── stage9_ablation/
        ├── WomenHealthAI_ablation_results_7day.json
        ├── WomenHealthAI_ablation_results_14day.json
        └── ablation_aggregate_results.csv
```

The two horizon-specific JSON files contain the recorded model results. The evaluator also writes a combined aggregate CSV containing the 7-day and 14-day comparisons.

## 2. Experimental Purpose

The ablation study evaluates the contribution of the five RHRS dimensions and two major model components:

- Hormonal Resilience Score (HRS)
- Physiological Resilience Score (PRS)
- Metabolic Resilience Score (MRS)
- Behavioral Resilience Score (BRS)
- Symptom Resilience Score (SRS)
- Temporal Attention
- Adaptive Variable Selection

The study also evaluates the effect of replacing the original RHRS weighting scheme with equal weighting.

For the dimension-removal ablations, the removed RHRS dimension is excluded from the model input while the canonical full RHRS target is retained. This isolates the effect of removing an input dimension from the forecasting model. The temporal-attention and adaptive-variable-selection ablations likewise retain the full RHRS target and modify only the corresponding model component. The equal-weight configuration is intentionally different: it changes the RHRS weighting definition and therefore evaluates target-weighting sensitivity rather than pure input removal.

Both 7-day and 14-day forecasting horizons are evaluated.

## 3. Ablation Configurations

| Configuration | Modification |
|---|---|
| `FULL` | Full WomenHealthAI configuration |
| `WO_HRS` | HRS removed from model inputs; full RHRS target retained |
| `WO_PRS` | PRS removed from model inputs; full RHRS target retained |
| `WO_MRS` | MRS removed from model inputs; full RHRS target retained |
| `WO_BRS` | BRS removed from model inputs; full RHRS target retained |
| `WO_SRS` | SRS removed from model inputs; full RHRS target retained |
| `EQUAL_WEIGHT_RHRS` | Equal RHRS weights used to define the target |
| `WO_TEMPORAL_ATTENTION` | Temporal Attention disabled; full RHRS target retained |
| `WO_ADAPTIVE_VARIABLE_SELECTION` | Adaptive Variable Selection disabled; full RHRS target retained |

## 4. RHRS Weighting

The original RHRS weights are:

```text
HRS = 0.25
PRS = 0.25
MRS = 0.15
BRS = 0.20
SRS = 0.15
```

The equal-weight configuration uses:

```text
HRS = 0.20
PRS = 0.20
MRS = 0.20
BRS = 0.20
SRS = 0.20
```

## 5. Forecasting Setup

The experiment uses a 14-day encoder window and evaluates:

- 7-day RHRS forecasting
- 14-day RHRS forecasting

The dataset is expected at:

```text
data/processed/rhrs_dataset.csv
```

## 6. Evaluation Metrics

Each experiment produces:

- MAE
- RMSE
- R²
- Pearson correlation coefficient (`r`)

## 7. How the Code Works

`ablation_config.py` defines the experimental configurations, RHRS weights, feature selection rules, horizons, and result paths.

`tft_ablation.py` independently loads the processed dataset, constructs forecasting sequences, applies each ablation, trains the ablation model, calculates the evaluation metrics, and writes the corresponding JSON result file directly into. Dimension-removal and architectural ablations retain the full RHRS target so their comparisons are aligned to the main forecasting target:

```text
results/stage9_ablation/
```

`evaluate_ablation.py` reads the two generated JSON files, prints the combined ablation results, and saves the aggregate comparison as `ablation_aggregate_results.csv`.

## 8. Generate the Results

Run both forecasting horizons:

```bash
python tft_ablation.py --horizon 7 14
```

This writes:

```text
../results/stage9_ablation/WomenHealthAI_ablation_results_7day.json
../results/stage9_ablation/WomenHealthAI_ablation_results_14day.json
```

A single horizon can also be executed:

```bash
python tft_ablation.py --horizon 7
```

or:

```bash
python tft_ablation.py --horizon 14
```

## 9. Inspect the Combined Ablation Results

After generating both JSON files:

```bash
python evaluate_ablation.py
```

The evaluator reads:

```text
../results/stage9_ablation/WomenHealthAI_ablation_results_7day.json
../results/stage9_ablation/WomenHealthAI_ablation_results_14day.json
```

and prints the combined result table while also saving the aggregate comparison to:

```text
../results/stage9_ablation/ablation_aggregate_results.csv
```

## 10. Result File Naming

The horizon-specific Stage 9 result files are:

```text
WomenHealthAI_ablation_results_7day.json
WomenHealthAI_ablation_results_14day.json
```

The aggregate comparison file is:

```text
ablation_aggregate_results.csv
```

No `(1)` suffix is used.

## 11. Interpretation of Ablation Results

The Stage 9 comparisons distinguish three experiment types:

- **Input-removal ablations:** one RHRS dimension is removed from the model input while the full RHRS target remains unchanged.
- **Model-component ablations:** Temporal Attention or Adaptive Variable Selection is disabled while the input representation and full RHRS target remain unchanged.
- **Target-weighting ablation:** equal weighting is used to construct RHRS, intentionally changing the target definition.

This distinction ensures that changes in forecasting performance are interpreted according to the part of the framework being varied.

## 11. Software Requirements

The training pipeline uses:

- Python
- NumPy
- pandas
- PyTorch

Install the required packages in the project environment before running the experiment.

## 13. Reproducibility

The Python implementation is independent of the recorded JSON artifacts and is designed to generate the two horizon-specific result files through model execution.

The supplied JSON files are retained as the recorded Stage 9 result artifacts. Rerunning the experiment can produce numerically different values unless the dataset, software environment, random seeds, hardware, and training configuration are controlled.
