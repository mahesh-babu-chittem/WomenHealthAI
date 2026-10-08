# 🌸 Stage 5 - Temporal Forecasting

> **Multimodal Reproductive Health Resilience Forecasting using
> Statistical, Machine Learning, and Deep Learning Models**

------------------------------------------------------------------------

## 🌟 Overview

Stage 5 is the **temporal forecasting component** of the WomenHealthAI
framework.

The objective of this stage is to forecast future **Reproductive Health
Resilience Score (RHRS)** from longitudinal multimodal observations.

The forecasting framework evaluates multiple model families under a
common temporal forecasting definition, a common temporal-window
construction strategy, and a common chronological evaluation protocol.

### 🤖 Models Included

-   📐 Linear Regression
-   🌲 Random Forest
-   🚀 XGBoost
-   🧠 LSTM
-   🔄 GRU
-   ↔️ BiLSTM
-   ⚡ Temporal Transformer
-   🎯 Temporal Fusion Transformer (TFT)

### 🔭 Forecasting Horizons

-   🔵 **H7** --- 7-day-ahead RHRS forecasting
-   🟣 **H14** --- 14-day-ahead RHRS forecasting

Both horizons use a fixed:

> **14-day historical encoder window**

------------------------------------------------------------------------

# 🎯 Objectives

Stage 5 has five primary objectives:

1.  📅 Construct scientifically consistent temporal forecasting windows.
2.  🔮 Forecast RHRS at both 7-day and 14-day horizons.
3.  ⚖️ Compare classical, machine-learning, and deep-learning models
    under the same evaluation protocol.
4.  📊 Evaluate forecasting performance using a comprehensive collection
    of metrics.
5.  🧪 Perform statistical comparisons using predictions corresponding
    to the same forecasting observations.

------------------------------------------------------------------------

# 🧭 Stage 5 Architecture

``` text
                    ┌──────────────────────────┐
                    │  Processed RHRS Dataset  │
                    │  rhrs_dataset.csv        │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Temporal Window Builder  │
                    │ create_temporal_windows  │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
             ┌──────────────┐          ┌──────────────┐
             │ H7 Windows   │          │ H14 Windows  │
             │ 14-day input │          │ 14-day input │
             │ + 7-day gap  │          │ +14-day gap  │
             └──────┬───────┘          └──────┬───────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Canonical Temporal Split │
                    │                          │
                    │ 70% Train                │
                    │ 15% Validation           │
                    │ 15% Test                 │
                    └────────────┬─────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────┐
        │              Forecasting Models                │
        │                                                │
        │ LR │ RF │ XGB │ LSTM │ GRU │ BiLSTM           │
        │ Transformer │ TFT                              │
        └───────────────────────┬────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────────┐
                    │ Prediction Generation    │
                    │                          │
                    │ Actual RHRS              │
                    │ Predicted RHRS           │
                    │ Temporal Metadata        │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┴─────────────┐
                    │                          │
                    ▼                          ▼
          ┌──────────────────┐       ┌──────────────────┐
          │ Performance      │       │ Statistical      │
          │ Evaluation       │       │ Comparison       │
          │                  │       │                  │
          │ MAE, RMSE, R²    │       │ Paired tests     │
          │ Correlation      │       │ Wilcoxon         │
          │ Trend metrics    │       │ Cohen's d        │
          └──────────────────┘       └──────────────────┘
```

------------------------------------------------------------------------

# 🧩 Forecasting Problem Definition

The Stage 5 forecasting task uses a fixed historical observation window
followed by a future forecasting horizon.

Let:

-   (W = 14) be the historical encoder length.
-   \(H\) be the forecasting horizon.
-   (H `\in `{=tex}{7,14}).
-   (RHRS_t) represent RHRS at time (t).

For each forecasting sample, the historical input is:

\[ X_i = {x_t,x\_{t+1},`\ldots`{=tex},x\_{t+W-1}} \]

with:

\[ W=14 \]

The target corresponds to the RHRS value at the selected forecasting
horizon:

\[ y_i = RHRS\_{t+W-1+H} \]

Therefore, the two forecasting tasks are defined as follows.

------------------------------------------------------------------------

# 🔵 H7 Forecasting

For H7, the model receives 14 historical observations and forecasts RHRS
7 days after the end of that historical window.

``` text
Historical Encoder Window
───────────────────────────────────────

Day t
Day t+1
Day t+2
...
Day t+12
Day t+13
              │
              │ 7-day forecasting horizon
              ▼
        Target RHRS
```

Formally:

\[ Target Day - Encoder End Day = 7 \]

------------------------------------------------------------------------

# 🟣 H14 Forecasting

For H14, the model receives the same 14-day historical encoder and
forecasts RHRS 14 days after the end of that historical window.

``` text
Historical Encoder Window
───────────────────────────────────────

Day t
Day t+1
Day t+2
...
Day t+12
Day t+13
              │
              │ 14-day forecasting horizon
              ▼
        Target RHRS
```

Formally:

\[ Target Day - Encoder End Day = 14 \]

------------------------------------------------------------------------

# 🪟 Temporal Window Construction

The temporal windows are generated by:

``` text
create_temporal_windows.py
```

The source dataset is:

``` text
data/
└── processed/
    └── rhrs_dataset.csv
```

The data are first ordered chronologically for each participant.

The temporal ordering is based on:

``` text
participant ID
+
day in study
```

This ensures that the generated forecasting windows represent actual
longitudinal sequences.

------------------------------------------------------------------------

# 📅 14-Day Historical Encoder

Every forecasting sample contains exactly 14 historical observations.

``` text
             14-Day Encoder
┌──────────────────────────────────────┐
│                                      │
│ Day 1  → Historical observation      │
│ Day 2  → Historical observation      │
│ Day 3  → Historical observation      │
│  ...                                 │
│ Day 14 → Historical observation      │
│                                      │
└──────────────────────────────────────┘
                  │
                  ▼
            Future RHRS
```

The same encoder definition is used for:

-   Linear Regression
-   Random Forest
-   XGBoost
-   LSTM
-   GRU
-   BiLSTM
-   Temporal Transformer
-   Temporal Fusion Transformer

------------------------------------------------------------------------

# 🔐 Temporal Integrity

The temporal-window construction performs explicit consistency checks.

## 1️⃣ Consecutive Encoder Observations

The 14-day historical encoder must contain consecutive study days.

For example:

``` text
Day 20
Day 21
Day 22
Day 23
...
Day 33
```

represents a contiguous 14-day sequence.

A sequence containing an internal temporal gap is not treated as an
equivalent contiguous encoder.

For example:

``` text
Day 20
Day 21
Day 23
Day 24
...
```

contains a gap between Day 21 and Day 23.

------------------------------------------------------------------------

## 2️⃣ Exact Forecast Horizon

For every generated forecasting window:

\[ Target Day - Encoder End Day = H \]

Therefore:

### H7

\[ Target Day - Encoder End Day = 7 \]

### H14

\[ Target Day - Encoder End Day = 14 \]

This makes the forecasting horizon an explicit temporal property rather
than simply a row-offset interpretation.

------------------------------------------------------------------------

## 3️⃣ Calendar-Date Validation

When calendar-date information is available, the window construction
also verifies the corresponding calendar-day relationships.

This prevents a simple row difference from being incorrectly interpreted
as an equivalent number of calendar days when observations are missing.

------------------------------------------------------------------------

# 📦 Generated Temporal Files

The temporal-window stage generates:

``` text
X_h7.npy
y_h7.npy

X_h14.npy
y_h14.npy
```

Metadata sidecars are also generated:

``` text
window_metadata_h7.csv
window_metadata_h14.csv
```

A diagnostic report is generated as:

``` text
windows_report.json
```

------------------------------------------------------------------------

# 🗂️ Window Metadata

Every generated forecasting window is associated with metadata.

The metadata include fields such as:

  Field                Description
  -------------------- --------------------------------------
  `participant_id`     Participant identifier
  `input_start_day`    First day of encoder window
  `input_end_day`      Last day of encoder window
  `target_day`         Forecast target day
  `target_date`        Forecast target date, when available
  `forecast_horizon`   H7 or H14
  `actual_rhrs`        Actual target RHRS
  `window_index`       Forecasting-window identifier

This metadata provides the link between the numerical forecasting arrays
and their temporal identity.

``` text
Numerical Window
       │
       ▼
Participant
       │
       ▼
Input Start Day
       │
       ▼
Input End Day
       │
       ▼
Target Day
       │
       ▼
Forecast Horizon
       │
       ▼
Actual RHRS
```

------------------------------------------------------------------------

# 🧱 Canonical Dataset Structure

Stage 5 uses a canonical temporal representation for each forecasting
horizon.

``` text
                  rhrs_dataset.csv
                         │
                         ▼
              Temporal Window Builder
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       H7 Temporal Set         H14 Temporal Set
             │                       │
             ▼                       ▼
        X_h7 / y_h7              X_h14 / y_h14
             │                       │
             └───────────┬───────────┘
                         │
                         ▼
                 Canonical Split
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
           Train      Validation    Test
            70%          15%         15%
```

------------------------------------------------------------------------

# ⏱️ Canonical Train / Validation / Test Split

The Stage 5 evaluation protocol uses:

  Split          Proportion
  ------------ ------------
  Training              70%
  Validation            15%
  Testing               15%

The split is chronological.

``` text
OLDER OBSERVATIONS
│
├────────────────────────────────────┤
│              TRAIN                 │
│               70%                  │
├────────────────────────────────────┤
│           VALIDATION               │
│               15%                  │
├────────────────────────────────────┤
│              TEST                  │
│               15%                 │
└────────────────────────────────────┘
                         → TIME
```

The chronological structure is maintained throughout the forecasting
pipeline.

------------------------------------------------------------------------

# ⚖️ Common Evaluation Observations

For a given forecasting horizon, all Stage 5 models operate on the same
canonical test observations.

Conceptually:

``` text
                         H7 Test Set
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 Linear Regression       Random Forest          XGBoost
        │                     │                     │
        ├─────────────────────┼─────────────────────┤
        │                     │                     │
        ▼                     ▼                     ▼
       LSTM                  GRU                  BiLSTM
        │                     │                     │
        ├─────────────────────┼─────────────────────┤
        │                     │                     │
        ▼                     ▼                     ▼
 Temporal Transformer          TFT
```

The same principle applies independently to H14.

This allows model performance to be compared under a common forecasting
population for each horizon.

------------------------------------------------------------------------

# 🤖 Forecasting Models

Stage 5 evaluates eight forecasting architectures.

------------------------------------------------------------------------

# 📐 1. Linear Regression

Linear Regression provides a classical statistical baseline.

The model maps the input representation to a continuous RHRS prediction.

``` text
Input Features
      │
      ▼
Linear Mapping
      │
      ▼
Predicted RHRS
```

### Output Files

``` text
linear_regression_results.json
linear_regression_predictions.csv
```

------------------------------------------------------------------------

# 🌲 2. Random Forest

Random Forest is an ensemble of decision trees.

``` text
                 Input
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Tree 1     Tree 2     Tree 3
        │          │          │
        └──────────┼──────────┘
                   ▼
             Ensemble
             Prediction
```

### Output Files

``` text
random_forest_results.json
random_forest_predictions.csv
```

------------------------------------------------------------------------

# 🚀 3. XGBoost

XGBoost uses gradient boosting to construct a sequence of decision
trees.

``` text
Initial Prediction
       │
       ▼
Residual Learning
       │
       ▼
Additional Tree
       │
       ▼
Residual Learning
       │
       ▼
Additional Tree
       │
       ▼
Final Prediction
```

### Output Files

``` text
xgboost_results.json
xgboost_predictions.csv
```

------------------------------------------------------------------------

# 🧠 4. LSTM

Long Short-Term Memory networks are designed to capture temporal
dependencies using recurrent gated processing.

``` text
x₁ ──► LSTM ──► h₁
x₂ ──► LSTM ──► h₂
x₃ ──► LSTM ──► h₃
...
x₁₄ ─► LSTM ──► h₁₄
                     │
                     ▼
                RHRS Prediction
```

### Output Files

``` text
lstm_results.json
lstm_predictions.csv
```

------------------------------------------------------------------------

# 🔄 5. GRU

Gated Recurrent Unit provides a recurrent architecture designed to model
temporal dependencies with a comparatively compact gating mechanism.

``` text
Historical Sequence
        │
        ▼
      GRU Cells
        │
        ▼
Temporal Representation
        │
        ▼
RHRS Prediction
```

### Output Files

``` text
gru_results.json
gru_predictions.csv
```

------------------------------------------------------------------------

# ↔️ 6. BiLSTM

Bidirectional LSTM processes the encoded sequence in both temporal
directions.

``` text
Forward:
x₁ → x₂ → x₃ → ... → x₁₄

Backward:
x₁₄ → x₁₃ → x₁₂ → ... → x₁

              │
              ▼
    Combined Representation
              │
              ▼
        RHRS Prediction
```

### Output Files

``` text
bilstm_results.json
bilstm_predictions.csv
```

------------------------------------------------------------------------

# ⚡ 7. Temporal Transformer

The Temporal Transformer uses attention-based sequence modeling to
capture relationships across the historical observations.

``` text
14-Day Sequence
      │
      ▼
Self-Attention
      │
      ▼
Temporal Representation
      │
      ▼
Prediction Head
      │
      ▼
Predicted RHRS
```

### Output Files

``` text
transformer_results.json
transformer_predictions.csv
```

------------------------------------------------------------------------

# 🎯 8. Temporal Fusion Transformer

The Temporal Fusion Transformer is an advanced temporal forecasting
architecture used for multimodal temporal modeling.

Its architecture incorporates mechanisms such as:

-   Variable selection
-   Gated processing
-   Temporal attention
-   Contextual information
-   Sequence modeling
-   Multi-horizon forecasting

Conceptually:

``` text
                 Multimodal Inputs
                        │
                        ▼
              Variable Selection
                        │
                        ▼
               Temporal Processing
                        │
                        ▼
                  Attention
                        │
                        ▼
               Temporal Representation
                        │
                        ▼
                 Forecast Decoder
                        │
                        ▼
                  Predicted RHRS
```

The Stage 5 TFT configuration uses:

``` text
Encoder Length = 14 days
```

and:

``` text
H7  → Prediction Horizon = 7
H14 → Prediction Horizon = 14
```

The TFT evaluation is aligned with the canonical temporal forecasting
windows.

### Output Files

The TFT result and prediction files are stored with the forecasting
horizon in their filenames to keep H7 and H14 artifacts distinct.

``` text
h{HORIZON}_tft_results.json
h{HORIZON}_tft_predictions.csv
```

------------------------------------------------------------------------

# 📊 Model Comparison Framework

Every model follows the same general evaluation structure.

``` text
Canonical Input
      │
      ▼
┌──────────────┐
│    Model     │
└──────┬───────┘
       │
       ▼
Predicted RHRS
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
Actual RHRS        Predicted RHRS
       │                 │
       └────────┬────────┘
                ▼
       Evaluation Metrics
```

The model architecture can differ, but the forecasting target and
evaluation observations remain consistent.

------------------------------------------------------------------------

# 📏 Evaluation Metrics

Stage 5 evaluates forecasting performance using regression, correlation,
trend, and risk-oriented metrics.

------------------------------------------------------------------------

## 📐 Regression Metrics

### Mean Absolute Error --- MAE

\[ MAE = `\frac{1}{N}`{=tex} `\sum`{=tex}\_{i=1}\^{N}
\|y_i-`\hat{y}`{=tex}\_i\| \]

Lower values indicate smaller average absolute prediction errors.

------------------------------------------------------------------------

### Mean Squared Error --- MSE

\[ MSE = `\frac{1}{N}`{=tex} `\sum`{=tex}\_{i=1}\^{N}
(y_i-`\hat{y}`{=tex}\_i)\^2 \]

Lower values indicate smaller squared prediction errors.

------------------------------------------------------------------------

### Root Mean Squared Error --- RMSE

\[ RMSE = `\sqrt{MSE}`{=tex} \]

RMSE places greater emphasis on larger prediction errors.

------------------------------------------------------------------------

### Mean Absolute Percentage Error --- MAPE

\[ MAPE = `\frac{100}{N}`{=tex} `\sum`{=tex}\_{i=1}\^{N} `\left`{=tex}\|
`\frac{y_i-\hat{y}_i}{y_i}`{=tex} `\right`{=tex}\| \]

------------------------------------------------------------------------

### Symmetric Mean Absolute Percentage Error --- SMAPE

\[ SMAPE = `\frac{100}{N}`{=tex} `\sum`{=tex}\_{i=1}\^{N}
`\frac{|y_i-\hat{y}_i|}`{=tex} {(\|y_i\|+\|`\hat{y}`{=tex}\_i\|)/2} \]

------------------------------------------------------------------------

### Median Absolute Error --- MedAE

The median of the absolute prediction errors.

MedAE provides a robust summary of typical prediction error and is less
influenced by extreme observations than mean-based measures.

------------------------------------------------------------------------

### Maximum Error

\[ MaxError = `\max`{=tex}\_i \|y_i-`\hat{y}`{=tex}\_i\| \]

This identifies the largest prediction deviation.

------------------------------------------------------------------------

### Coefficient of Determination --- (R\^2)

\[ R\^2 = 1- `\frac{
\sum_i(y_i-\hat{y}_i)^2
}{
\sum_i(y_i-\bar{y})^2
}`{=tex} \]

Higher values indicate greater explained variance.

------------------------------------------------------------------------

# 🔗 Correlation Metrics

Stage 5 also evaluates the relationship between actual and predicted
RHRS.

### Pearson Correlation

Measures linear association between actual and predicted RHRS.

### Spearman Correlation

Measures rank-based monotonic association.

### Kendall Correlation

Measures ordinal association based on concordant and discordant pairs.

------------------------------------------------------------------------

# 📈 Trend Metrics

Forecasting quality can also be assessed according to whether the model
correctly captures the direction of change.

The framework includes:

-   Trend Accuracy
-   Trend Precision
-   Trend Recall
-   Trend F1

Conceptually:

``` text
Actual RHRS

       ↗
      /
─────●────────
    /
   ↘


Predicted RHRS

       ↗
      /
─────●────────
    /
   ↘
```

The trend metrics evaluate whether predicted changes are consistent with
actual changes.

------------------------------------------------------------------------

# ⚠️ Risk-Oriented Metrics

The forecasting outputs can additionally be evaluated using threshold-
or category-based measures.

These include:

-   Accuracy
-   Precision
-   Recall
-   F1
-   Balanced Accuracy
-   MCC
-   Cohen's Kappa
-   True Positive Rate
-   False Positive Rate
-   True Negative Rate
-   False Negative Rate

These metrics complement continuous regression metrics by providing an
additional view of prediction behavior.

------------------------------------------------------------------------

# 🧪 Statistical Comparison

Stage 5 includes statistical comparison between model predictions.

The statistical analysis includes:

-   📊 Paired t-test
-   📊 Wilcoxon signed-rank test
-   📏 Cohen's (d)

The comparisons are performed using corresponding forecasting
observations.

------------------------------------------------------------------------

# 🔗 Matched Prediction Identity

Predictions are matched using:

``` text
participant_id
+
target_day
+
forecast_horizon
```

This combination identifies a specific forecasting observation.

For example:

``` text
Participant: P017
Target Day: 91
Forecast Horizon: H7
```

represents one specific forecasting instance.

The prediction for that same participant, target day, and horizon is
therefore directly comparable across models within the authorized
analysis environment.

------------------------------------------------------------------------

# 🔬 Paired Error Analysis

For a matched observation:

\[ e_i\^{(A)} = y_i-`\hat{y}`{=tex}\_i\^{(A)} \]

and:

\[ e_i\^{(B)} = y_i-`\hat{y}`{=tex}\_i\^{(B)} \]

The statistical comparison is then performed over corresponding paired
errors:

\[ (e_1^{(A)},e_1^{(B)}), `\ldots`{=tex}, (e_N^{(A)},e_N^{(B)}) \]

This ensures that model comparisons are based on the same forecasting
observations.

------------------------------------------------------------------------

# 🚫 No Arbitrary Positional Matching

Prediction arrays are not compared merely because their row positions
happen to be identical.

For example, the following is not sufficient:

``` text
Model A row 1 ↔ Model B row 1
Model A row 2 ↔ Model B row 2
...
```

Instead, observations are matched through their explicit identifiers:

``` text
participant_id
target_day
forecast_horizon
```

This provides observation-level traceability.

------------------------------------------------------------------------

# 🔐 Actual RHRS Consistency

When predictions are matched, the actual RHRS associated with the same
forecasting observation must also agree.

Conceptually:

``` text
                Same Observation
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
      Model A                   Model B
          │                         │
          ▼                         ▼
    Actual RHRS                Actual RHRS
          │                         │
          └────────────┬────────────┘
                       ▼
                 Consistency Check
```

This prevents accidental comparison of predictions against different
ground-truth values.

------------------------------------------------------------------------

# 📊 Statistical Testing Pipeline

``` text
Model A Predictions
        │
        ▼
Prediction Keys
        │
        ├───────────────────┐
        │                   │
        ▼                   ▼
Model B Predictions     Model B Keys
        │                   │
        └─────────┬─────────┘
                  ▼
            Key Matching
                  │
                  ▼
        Matched Observations
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
    Paired      Wilcoxon   Cohen's
    t-test       Test        d
```

------------------------------------------------------------------------

# 🗃️ Statistical Output Files

The statistical comparison stage generates:

``` text
Table_18_Statistical_Significance.csv
Table_19_Significant_Comparisons.csv
```

These contain the model-comparison statistics generated from matched
prediction observations.

------------------------------------------------------------------------

# 🧾 Prediction File Structure

Each forecasting model produces a prediction CSV containing the
prediction and its associated temporal metadata.

Typical fields include:

  -----------------------------------------------------------------------
  Column                              Description
  ----------------------------------- -----------------------------------
  `Actual_RHRS` / `Actual`            Ground-truth RHRS

  `Predicted_RHRS` / `Predicted`      Model prediction

  `participant_id`                    Internal participant identifier
                                      used for observation matching

  `target_date`                       Target calendar date used in
                                      internal temporal validation

  `target_day`                        Target study day

  `input_start_day`                   Encoder start day

  `input_end_day`                     Encoder end day

  `forecast_horizon`                  H7 or H14

  `window_index`                      Canonical window identifier
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 🔍 Prediction Traceability

Every prediction can be traced through:

``` text
Prediction
    │
    ▼
Model
    │
    ▼
Forecast Horizon
    │
    ▼
Participant
    │
    ▼
Target Day
    │
    ▼
Input Start Day
    │
    ▼
Input End Day
    │
    ▼
Actual RHRS
```

This makes prediction-level auditing and statistical analysis possible.

Participant-level identifiers and individual prediction records are used
only within the authorized analysis environment. They are not intended
to be redistributed in the public repository; public releases should
retain only approved aggregate results and non-identifying
methodological artifacts.

------------------------------------------------------------------------

# 📁 Stage 5 Directory Structure

``` text
stage5_forecasting/
│
├── README.md
│
├── config.py
├── create_temporal_windows.py
├── evaluation_utils.py
├── metrics_regression.py
├── statistical_significance.py
├── torch_dataset.py
│
├── linear_regression_model.py
├── random_forest_model.py
├── xgboost_model.py
├── lstm_model.py
├── gru_model.py
├── bilstm_model.py
├── temporal_transformer.py
└── tft_model.py
```

The generated outputs are stored under:

``` text
results/
└── stage5_forecasting/
```

Participant-level prediction files and temporal metadata are analysis
artifacts and should only be retained or shared when permitted by the
applicable data access conditions.

------------------------------------------------------------------------

# 📦 Generated Output Structure

``` text
results/
└── stage5_forecasting/
    │
    ├── X_h7.npy
    ├── y_h7.npy
    ├── window_metadata_h7.csv
    │
    ├── X_h14.npy
    ├── y_h14.npy
    ├── window_metadata_h14.csv
    │
    ├── windows_report.json
    │
    ├── linear_regression_results.json
    ├── linear_regression_predictions.csv
    │
    ├── random_forest_results.json
    ├── random_forest_predictions.csv
    │
    ├── xgboost_results.json
    ├── xgboost_predictions.csv
    │
    ├── lstm_results.json
    ├── lstm_predictions.csv
    │
    ├── gru_results.json
    ├── gru_predictions.csv
    │
    ├── bilstm_results.json
    ├── bilstm_predictions.csv
    │
    ├── transformer_results.json
    ├── transformer_predictions.csv
    │
    ├── tft_results.json
    ├── tft_predictions.csv
    │
    ├── Table_18_Statistical_Significance.csv
    └── Table_19_Significant_Comparisons.csv
```

------------------------------------------------------------------------

# ⚙️ Configuration

The primary forecasting configuration is controlled through:

``` text
config.py
```

Important configuration parameters include:

``` python
HORIZON = 14

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15
```

For H7 experiments:

``` python
HORIZON = 7
```

For H14 experiments:

``` python
HORIZON = 14
```

------------------------------------------------------------------------

# 🔄 H7 Execution

## Step 1 --- Select H7

Set:

``` python
HORIZON = 7
```

------------------------------------------------------------------------

## Step 2 --- Generate Temporal Windows

Run:

``` bash
python create_temporal_windows.py
```

This generates the canonical H7 representation and metadata.

------------------------------------------------------------------------

## Step 3 --- Run All Models

Execute:

``` text
linear_regression_model.py
random_forest_model.py
xgboost_model.py
lstm_model.py
gru_model.py
bilstm_model.py
temporal_transformer.py
tft_model.py
```

------------------------------------------------------------------------

## Step 4 --- Validate Predictions

Verify that the generated predictions contain:

-   Actual RHRS
-   Predicted RHRS
-   Participant ID
-   Target day
-   Forecast horizon
-   Encoder information

------------------------------------------------------------------------

## Step 5 --- Preserve H7 Results

Store the completed H7 and H14 result sets separately so that files from
one forecasting horizon cannot overwrite or be confused with those from
the other horizon.

A convenient organization is:

``` text
results/
└── stage5_forecasting/
    ├── H7/
    │   ├── model results
    │   ├── predictions
    │   └── statistical outputs
    │
    └── H14/
```

------------------------------------------------------------------------

# 🔄 H14 Execution

## Step 1 --- Select H14

Set:

``` python
HORIZON = 14
```

------------------------------------------------------------------------

## Step 2 --- Generate H14 Windows

Run:

``` bash
python create_temporal_windows.py
```

This generates the canonical H14 representation and metadata.

------------------------------------------------------------------------

## Step 3 --- Run All Models

Execute:

``` text
linear_regression_model.py
random_forest_model.py
xgboost_model.py
lstm_model.py
gru_model.py
bilstm_model.py
temporal_transformer.py
tft_model.py
```

------------------------------------------------------------------------

## Step 4 --- Validate Predictions

Verify the temporal identifiers and prediction values.

------------------------------------------------------------------------

## Step 5 --- Preserve H14 Results

Archive the H14 results separately from H7 results.

------------------------------------------------------------------------

# 🔁 Recommended Complete Execution Order

``` text
                         START
                           │
                           ▼
              Check processed dataset
                           │
                           ▼
                   Set HORIZON = 7
                           │
                           ▼
              Generate H7 windows
                           │
                           ▼
              Run all Stage 5 models
                           │
                           ▼
                 Preserve H7 results
                           │
                           ▼
                  Set HORIZON = 14
                           │
                           ▼
             Generate H14 windows
                           │
                           ▼
             Run all Stage 5 models
                           │
                           ▼
                Preserve H14 results
                           │
                           ▼
           Run statistical comparisons
                           │
                           ▼
             Generate final tables
                           │
                           ▼
                          END
```

------------------------------------------------------------------------

# 🧪 Reproducibility Checklist

## 📂 Dataset

-   [ ] Correct processed dataset is available.
-   [ ] Participant identifiers are preserved.
-   [ ] Temporal ordering is preserved.
-   [ ] RHRS values are available.

## 🪟 Temporal Windows

-   [ ] Encoder length is 14 days.
-   [ ] Encoder observations are consecutive.
-   [ ] H7 target gap is exactly 7 days.
-   [ ] H14 target gap is exactly 14 days.
-   [ ] Window metadata match the generated arrays.

## ✂️ Data Splitting

-   [ ] Training = 70%.
-   [ ] Validation = 15%.
-   [ ] Testing = 15%.
-   [ ] Chronological order is preserved.

## 🤖 Models

-   [ ] Linear Regression executed.
-   [ ] Random Forest executed.
-   [ ] XGBoost executed.
-   [ ] LSTM executed.
-   [ ] GRU executed.
-   [ ] BiLSTM executed.
-   [ ] Temporal Transformer executed.
-   [ ] TFT executed.

## 📊 Predictions

-   [ ] Actual RHRS is present.
-   [ ] Predicted RHRS is present.
-   [ ] Internal observation identifiers are available when authorized.
-   [ ] Target day is available for internal matching.
-   [ ] Forecast horizon is present.
-   [ ] Prediction identities are unique within the authorized analysis
    environment.

## 🧪 Statistics

-   [ ] Predictions are matched by participant.
-   [ ] Predictions are matched by target day.
-   [ ] Predictions are matched by horizon.
-   [ ] Actual RHRS values are consistent.
-   [ ] Paired tests use matched observations.
-   [ ] Statistical result files are generated.

------------------------------------------------------------------------

# 🛡️ Data Leakage Prevention

Stage 5 is designed as a chronological forecasting problem.

The fundamental structure is:

``` text
PAST
 │
 ▼
Training
 │
 ▼
Validation
 │
 ▼
Testing
 │
 ▼
FUTURE
```

The forecasting process maintains the temporal ordering of the
observations.

The target is also explicitly separated from the historical encoder
according to the selected forecasting horizon.

------------------------------------------------------------------------

# 🧠 Model Families

Stage 5 intentionally covers multiple levels of model complexity.

``` text
                    Forecasting Models
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
         Classical     Machine        Deep Learning
          Models       Learning
             │             │             │
             ▼             ▼             ▼
      Linear Regression  Random Forest  LSTM
                         XGBoost        GRU
                                        BiLSTM
                                        Transformer
                                        TFT
```

This provides a broad comparison across statistical, machine-learning,
and deep-learning forecasting approaches.

------------------------------------------------------------------------

# 🌐 Multimodal Temporal Forecasting

The broader WomenHealthAI framework integrates multimodal
reproductive-health information.

The Stage 5 forecasting component operates on the resulting temporal
representations.

Conceptually:

``` text
Physiological Information
          │
Behavioral Information
          │
Metabolic Information
          │
Hormonal Information
          │
Symptom Information
          │
          ▼
Multimodal Representation
          │
          ▼
Temporal Window
          │
          ▼
Forecasting Model
          │
          ▼
Future RHRS
```

------------------------------------------------------------------------

# 📅 Forecasting Horizons and Interpretation

### 🔵 H7

H7 estimates the future RHRS approximately one week after the historical
encoder window.

### 🟣 H14

H14 estimates the future RHRS approximately two weeks after the
historical encoder window.

Both tasks use the same 14-day historical context.

------------------------------------------------------------------------

# 📈 Interpreting the Metrics

The metrics should be interpreted together rather than relying on a
single value.

  Metric                     Preferred Direction Interpretation
  ------------------------ --------------------- -----------------------------------
  MAE                                          ↓ Smaller average absolute error
  MSE                                          ↓ Smaller squared error
  RMSE                                         ↓ Lower sensitivity to large errors
  MAPE                                         ↓ Lower percentage error
  SMAPE                                        ↓ Lower symmetric percentage error
  MedAE                                        ↓ Lower typical absolute error
  MaxError                                     ↓ Lower worst-case error
  (R\^2)                                       ↑ Greater explained variance
  Pearson (r)                                  ↑ Stronger linear association
  Spearman (r)                                 ↑ Stronger rank association
  Kendall (`\tau`{=tex})                       ↑ Stronger ordinal association
  Trend Accuracy                               ↑ Better direction prediction
  Trend F1                                     ↑ Better balanced trend detection

------------------------------------------------------------------------

# 🧮 Why Multiple Metrics Are Used

Different metrics capture different aspects of forecasting behavior.

For example:

``` text
MAE
 │
 └── Average absolute prediction error

RMSE
 │
 └── Greater sensitivity to large errors

R²
 │
 └── Explained variance

Correlation
 │
 └── Association between actual and predicted values

Trend Metrics
 │
 └── Directional consistency

Risk Metrics
 │
 └── Threshold/category behavior
```

Using multiple metrics provides a more complete evaluation of
forecasting performance.

------------------------------------------------------------------------

# 🧪 Statistical Comparison Philosophy

Statistical comparison focuses on the same forecasting observations.

For a particular observation:

``` text
Same Participant
        +
Same Target Day
        +
Same Horizon
        +
Same Actual RHRS
        │
        ▼
 ┌──────┴──────┐
 │             │
 ▼             ▼
Model A       Model B
Prediction    Prediction
 │             │
 ▼             ▼
Error A       Error B
 └──────┬──────┘
        ▼
 Paired Comparison
```

This makes the comparison observation-aware rather than merely
array-position-aware.

------------------------------------------------------------------------

# 🧰 Utility Modules

## `evaluation_utils.py`

Provides shared evaluation infrastructure including:

-   Canonical split loading
-   Prediction saving
-   Prediction-file discovery
-   Prediction-key construction
-   Matched-observation handling

------------------------------------------------------------------------

## `metrics_regression.py`

Provides the regression and forecasting metrics used by the Stage 5
models.

The shared metric implementation ensures consistent metric definitions
across models.

------------------------------------------------------------------------

## `statistical_significance.py`

Performs statistical comparisons using:

-   Paired t-test
-   Wilcoxon signed-rank test
-   Cohen's (d)

The comparison process is based on explicit prediction identities.

------------------------------------------------------------------------

## `torch_dataset.py`

Provides the dataset wrapper used by the PyTorch-based forecasting
models.

------------------------------------------------------------------------

# 📋 Model Summary

  ---------------------------------------------------------------------------
  Model            Family               Temporal Modeling Primary Role
  ---------------- ---------------- --------------------- -------------------
  Linear           Statistical                         ❌ Classical baseline
  Regression                                              

  Random Forest    Ensemble ML                         ❌ Nonlinear baseline

  XGBoost          Boosting                            ❌ Gradient-boosting
                                                          baseline

  LSTM             Recurrent DL                        ✅ Sequential
                                                          dependency modeling

  GRU              Recurrent DL                        ✅ Efficient recurrent
                                                          modeling

  BiLSTM           Bidirectional                       ✅ Bidirectional
                   RNN                                    sequence modeling

  Temporal         Attention                           ✅ Attention-based
  Transformer                                             temporal modeling

  TFT              Temporal DL                         ✅ Advanced multimodal
                                                          forecasting
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

# 🔄 End-to-End Workflow

``` text
                         ┌─────────────────┐
                         │ Processed Data  │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │ Temporal Window Builder │
                    └────────────┬────────────┘
                                 │
                     ┌───────────┴───────────┐
                     │                       │
                     ▼                       ▼
                    H7                      H14
                     │                       │
                     ▼                       ▼
              Canonical Split        Canonical Split
                     │                       │
                     ▼                       ▼
              ┌─────────────┐         ┌─────────────┐
              │ 8 Models    │         │ 8 Models    │
              └──────┬──────┘         └──────┬──────┘
                     │                       │
                     ▼                       ▼
               Predictions             Predictions
                     │                       │
                     └──────────┬────────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Evaluation Metrics  │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Matched Statistics  │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Final Results       │
                     └─────────────────────┘
```

------------------------------------------------------------------------

# 📚 Relationship to WomenHealthAI

Stage 5 forms the temporal forecasting component of the larger
WomenHealthAI framework.

``` text
┌─────────────────────────────────────────────────────┐
│                  WomenHealthAI                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Multimodal Data                                   │
│          │                                          │
│          ▼                                          │
│  Preprocessing                                      │
│          │                                          │
│          ▼                                          │
│  RHRS Construction                                  │
│          │                                          │
│          ▼                                          │
│  Temporal Window Generation                         │
│          │                                          │
│          ▼                                          │
│  ┌─────────────────────────────────────────────┐    │
│  │             Stage 5 Forecasting             │    │
│  │                                             │    │
│  │ LR │ RF │ XGB │ LSTM │ GRU │ BiLSTM        │    │
│  │ Transformer │ TFT                           │    │
│  └─────────────────────┬───────────────────────┘    │
│                        │                            │
│                        ▼                            │
│                  Future RHRS                        │
│                        │                            │
│                        ▼                            │
│              Downstream Analysis                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

------------------------------------------------------------------------

# 🏁 Key Takeaways

### 🪟 Fixed Historical Context

Every forecasting sample uses:

``` text
14-day historical encoder
```

------------------------------------------------------------------------

### 🔭 Two Forecasting Horizons

``` text
H7  → 7-day-ahead forecasting
H14 → 14-day-ahead forecasting
```

------------------------------------------------------------------------

### ⏱️ Chronological Evaluation

``` text
70% Training
15% Validation
15% Testing
```

------------------------------------------------------------------------

### 🤖 Eight Forecasting Models

``` text
Linear Regression
Random Forest
XGBoost
LSTM
GRU
BiLSTM
Temporal Transformer
Temporal Fusion Transformer
```

------------------------------------------------------------------------

### 📊 Comprehensive Evaluation

Stage 5 evaluates:

``` text
Regression
Correlation
Trend
Risk
Statistical Significance
```

------------------------------------------------------------------------

### 🔗 Explicit Observation Matching

Prediction-level comparisons use:

``` text
participant_id
+
target_day
+
forecast_horizon
```

------------------------------------------------------------------------

### 🔁 Reproducible Pipeline

The complete workflow is:

``` text
Dataset
  ↓
Temporal Windows
  ↓
Canonical Split
  ↓
Model Training
  ↓
Predictions
  ↓
Metrics
  ↓
Matched Statistical Analysis
  ↓
Final Results
```

------------------------------------------------------------------------

# 🏆 Stage 5 Summary

The Stage 5 temporal forecasting framework can be summarized
mathematically as:

\[ `\boxed{
14\text{-day historical window}
\rightarrow
RHRS_{t+H}
}`{=tex} \]

where:

\[ H `\in `{=tex}{7,14} \]

The forecasting experiments use:

\[ `\boxed{
70\%\ Training
+
15\%\ Validation
+
15\%\ Testing
}`{=tex} \]

and compare:

\[ `\boxed{
\{
LR,\ RF,\ XGB,\ LSTM,\ GRU,\ BiLSTM,\ Transformer,\ TFT
\}
}`{=tex} \]

with prediction-level identification through:

\[ `\boxed{
(
participant\_id,\ target\_day,\ forecast\_horizon
)
}`{=tex} \]

------------------------------------------------------------------------

# 📌 Final Stage 5 Status

  Component                       Status
  ------------------------------- --------
  Multimodal RHRS Dataset         ✅
  14-Day Encoder Windows          ✅
  H7 Forecasting                  ✅
  H14 Forecasting                 ✅
  Canonical Temporal Split        ✅
  Linear Regression               ✅
  Random Forest                   ✅
  XGBoost                         ✅
  LSTM                            ✅
  GRU                             ✅
  BiLSTM                          ✅
  Temporal Transformer            ✅
  Temporal Fusion Transformer     ✅
  Prediction Metadata             ✅
  Regression Metrics              ✅
  Correlation Metrics             ✅
  Trend Metrics                   ✅
  Risk Metrics                    ✅
  Matched Statistical Testing     ✅
  Reproducible Output Structure   ✅

------------------------------------------------------------------------

# 🌸 WomenHealthAI

> **Forecasting reproductive health resilience through multimodal
> temporal intelligence.**

``` text
Multimodal Data
      ↓
RHRS
      ↓
Temporal Windows
      ↓
H7 / H14 Forecasting
      ↓
Multiple Model Families
      ↓
Common Evaluation
      ↓
Matched Statistical Analysis
      ↓
Future Reproductive Health Resilience
```

------------------------------------------------------------------------

## 📁 Stage 5 Core Files

``` text
create_temporal_windows.py
evaluation_utils.py
metrics_regression.py
statistical_significance.py
torch_dataset.py

linear_regression_model.py
random_forest_model.py
xgboost_model.py
lstm_model.py
gru_model.py
bilstm_model.py
temporal_transformer.py
tft_model.py

config.py
README.md
```

------------------------------------------------------------------------

> **Stage 5 provides the complete temporal forecasting infrastructure
> for WomenHealthAI, from canonical temporal-window construction and
> model training to prediction-level evaluation and statistically
> matched model comparison.**
