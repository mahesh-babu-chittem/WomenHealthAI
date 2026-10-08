# 🔍 Stage 6 --- Explainability Analysis

> **Purpose:** Interpret the Temporal Fusion Transformer (TFT) used for
> multi-horizon Reproductive Health Resilience Score (RHRS) forecasting
> through feature importance, temporal attention, global explanations,
> local explanations, and SHAP-based attribution.

Stage 6 forms the **explainability component of the WomenHealthAI
framework**.

The explainability pipeline is applied to the trained TFT forecasting
model used for the two forecasting horizons evaluated in the study:

-   🔭 **7-day RHRS forecasting**
-   🔭 **14-day RHRS forecasting**

Both experiments use a **14-day historical input window**.

The forecasting horizon is configured manually before each experimental
run, following the same procedure used in Stage 5.

------------------------------------------------------------------------

# 📌 Stage Overview

The complete Stage 6 workflow is:

**Stage 5 TFT Model → Horizon Configuration → Feature Importance →
Temporal Attention → Global Explanation → Local Explanation → SHAP
Analysis**

  -----------------------------------------------------------------------
  Component                           Description
  ----------------------------------- -----------------------------------
  📥 Input                            RHRS-enriched longitudinal dataset

  🤖 Forecasting model                Temporal Fusion Transformer

  🪟 Historical window                14 days

  🔭 Forecast horizon                 7 days or 14 days

  🔧 Horizon configuration            Manually changed between
                                      experimental runs

  🧬 Feature explanation              TFT feature importance

  ⏱️ Temporal explanation             TFT temporal attention

  🌎 Global explanation               Top features and attention
                                      positions

  👤 Local explanation                Example participant/prediction
                                      explanation

  🧮 SHAP                             Feature-attribution analysis

  📊 Main manuscript figure           Figure 4

  📋 Main manuscript table            Table VI
  -----------------------------------------------------------------------

The manuscript describes the forecasting framework as a multi-horizon
TFT with:

    H ∈ {7, 14}

while using:

    W = 14

for the historical sliding window.

------------------------------------------------------------------------

# 📂 Directory Structure

    stage6_explainability/
    │
    ├── feature_importance.py
    ├── attention_analysis.py
    ├── global_explanations.py
    ├── local_explanations.py
    ├── shap_analysis.py
    │
    └── README.md

Stage 6 writes its generated artifacts to:

    results/
    └── stage6_explainability/

The explainability scripts use the trained TFT checkpoint produced
during Stage 5:

    results/
    └── stage5_forecasting/
        └── checkpoints/
            └── tft_final.ckpt

------------------------------------------------------------------------

# 1️⃣ Input Dataset

Stage 6 uses the processed RHRS dataset:

    data/processed/rhrs_dataset.csv

The dataset is ordered using:

    id
    day_in_study

A participant-specific temporal index is then reconstructed using the
chronological observations for each participant.

The dataset contains the multimodal variables used throughout the
WomenHealthAI framework, including:

-   Hormonal measurements
-   HRV measurements
-   Resting heart rate
-   Glucose measurements
-   Sleep measurements
-   Stress measurements
-   RHRS dimensions
-   Overall RHRS

------------------------------------------------------------------------

# 2️⃣ Multi-Horizon Experimental Configuration

The Stage 6 explainability analysis follows the same multi-horizon
experimental design as Stage 5.

The historical encoder window remains fixed at:

    14 days

The forecasting horizon is changed manually between experiments.

------------------------------------------------------------------------

## 🔵 Experiment 1 --- 7-Day Forecasting

Before executing the H7 experiment, the forecasting configuration is set
to:

    HORIZON = 7

For the TFT configuration:

    max_prediction_length = 7

The TFT experiment is then executed and the corresponding H7
model/prediction artifacts are produced.

The explainability scripts can subsequently be run on the corresponding
trained TFT configuration.

------------------------------------------------------------------------

## 🟣 Experiment 2 --- 14-Day Forecasting

For the H14 experiment, the configuration is manually changed to:

    HORIZON = 14

For the TFT configuration:

    max_prediction_length = 14

The TFT experiment is then executed again.

The corresponding H14 model/prediction artifacts are produced and can
subsequently be analyzed using the Stage 6 explainability scripts.

------------------------------------------------------------------------

# 3️⃣ Experimental Relationship Between H7 and H14

The two experiments therefore follow:

    14-day historical window
              │
       ┌──────┴──────┐
       │             │
    HORIZON = 7   HORIZON = 14
       │             │
       ▼             ▼
      H7 TFT        H14 TFT
       │             │
       ▼             ▼
    H7 Forecast    H14 Forecast
       │             │
       └──────┬──────┘
              ▼
        Explainability

The horizon is not changed dynamically during one execution.

Instead, the experiment is configured for the required horizon,
executed, and the corresponding outputs are generated.

The same procedure is repeated for the second horizon.

------------------------------------------------------------------------

# 4️⃣ Stage 5 Dependency

Stage 6 does not train the forecasting model from scratch.

Instead, it analyzes the trained TFT model produced by Stage 5.

The dependency is:

    Stage 5
       │
       ▼
    Temporal Forecasting
       │
       ▼
    Trained TFT
       │
       ▼
    Stage 6
       │
       ├── Feature Importance
       ├── Temporal Attention
       ├── Global Explanation
       ├── Local Explanation
       └── SHAP Analysis

Therefore, Stage 5 should be completed before executing Stage 6.

------------------------------------------------------------------------

# 5️⃣ Feature Importance Analysis

### Script

    feature_importance.py

This script extracts feature-level importance information from the
trained TFT.

The TFT is loaded from:

    results/stage5_forecasting/checkpoints/tft_final.ckpt

The model is evaluated without additional training.

The interpretation is obtained from the TFT model's raw output and
interpretation mechanism.

The feature importance representation corresponds to the encoder
variables used by the TFT.

------------------------------------------------------------------------

# 6️⃣ TFT Features Used for Interpretation

The explainability pipeline considers the following variables. These
variables are the feature representation used for the explainability
analyses and do not imply that every variable contributes directly to
every TFT component:

  Category                   Variables
  -------------------------- ------------------------------
  🎯 RHRS                    RHRS
  🧩 Resilience dimensions   HRS, PRS, MRS, BRS, SRS
  🧬 Hormonal                lh, estrogen, pdg
  ❤️ HRV                     mean_rmssd, mean_lf, mean_hf
  🩸 Glucose                 mean_glucose, std_glucose
  💓 Cardiovascular          resting_hr
  😴 Sleep                   sleep_score, deep_sleep
  😟 Stress                  stress_score

These variables correspond to the multimodal representation used by the
forecasting framework.

------------------------------------------------------------------------

# 7️⃣ TFT Feature Importance Extraction

The TFT interpretation process obtains the model's encoder-variable
importance representation.

The resulting importance values are associated with their corresponding
feature names.

The values are then sorted in descending order.

The resulting table contains:

    Feature
    Importance

------------------------------------------------------------------------

# 8️⃣ Feature Importance Output

The feature importance table is stored as:

    results/stage6_explainability/
    └── Table_22_Feature_Importance.csv

The corresponding visualization is:

    results/stage6_explainability/
    └── Figure_12_Feature_Importance.png

The figure presents the relative importance of the variables used by the
TFT.

------------------------------------------------------------------------

# 9️⃣ Manuscript Feature Importance Results

The manuscript reports the following feature-importance values in Table
VI:

  Feature         TFT Feature Importance
  ------------- ------------------------
  mean rmssd                      420.03
  sleep score                     380.87
  SRS                             354.85
  MRS                             349.28
  mean lf                         326.07
  RHRS                            307.69
  mean hf                         307.03
  HRS                             298.15
  resting hr                      291.96
  BRS                             252.42

The manuscript describes RMSSD, sleep score, SRS, MRS, and low-frequency
HRV among the dominant contributors identified by the explainability
analysis.

------------------------------------------------------------------------

# 🔟 Temporal Attention Analysis

### Script

    attention_analysis.py

This script extracts temporal attention information from the TFT
interpretation output.

The analysis uses the historical encoder sequence.

The historical window is:

    14 days

The attention values therefore represent the relative attention assigned
to positions within the historical temporal context.

------------------------------------------------------------------------

# 1️⃣1️⃣ Temporal Attention Representation

Historical positions are represented relative to the forecasting point.

Examples include:

    0
    -1
    -2
    -3
    ...
    -13

where:

    0  = most recent historical position
    -1 = one position earlier
    -2 = two positions earlier

and so on.

The resulting attention table contains:

    Historical_Day
    Attention_Weight

------------------------------------------------------------------------

# 1️⃣2️⃣ Attention Output

The attention table is stored as:

    results/stage6_explainability/
    └── Table_23_Attention_Weights.csv

The corresponding visualization is:

    results/stage6_explainability/
    └── Figure_13_Attention_Weights.png

The figure illustrates how the TFT distributes attention across the
historical window.

------------------------------------------------------------------------

# 1️⃣3️⃣ Manuscript Attention Results

The manuscript reports the following attention values in Table VI:

    Historical Day   Attention Weight
  ---------------- ------------------
                 0             0.0805
                -1             0.0776
                -8             0.0761
                -2             0.0758
                -7             0.0757
                -6             0.0754
                -3             0.0751
                -9             0.0747
                -4             0.0746
                -5             0.0744

The manuscript describes the attention pattern as emphasizing recent
observations while also incorporating information from earlier
observations approximately one week before the forecasting point.

------------------------------------------------------------------------

# 1️⃣4️⃣ Global Explanation

### Script

    global_explanations.py

The global explanation stage combines the outputs from:

    Table_22_Feature_Importance.csv

and:

    Table_23_Attention_Weights.csv

The purpose is to summarize the model's interpretation at the global
level.

------------------------------------------------------------------------

# 1️⃣5️⃣ Top Global Features

The feature-importance table is sorted by importance.

The top ten features are extracted.

Output:

    results/stage6_explainability/
    └── Table_24_Top10_Features.csv

The table contains:

    Feature
    Importance

This provides a compact representation of the most influential variables
identified by the TFT.

------------------------------------------------------------------------

# 1️⃣6️⃣ Top Temporal Attention Positions

The attention table is sorted by attention weight.

The top ten historical positions are extracted.

Output:

    results/stage6_explainability/
    └── Table_25_Top10_Attention_Days.csv

The table contains:

    Historical_Day
    Attention_Weight

------------------------------------------------------------------------

# 1️⃣7️⃣ Global Explanation Figure

The global explanation visualization combines:

    Feature Importance

and:

    Temporal Attention

The resulting figure is:

    results/stage6_explainability/
    └── Figure_14_Global_Explanations.png

This provides a combined global view of:

    Which variables are influential

and:

    Which historical positions receive greater attention

------------------------------------------------------------------------

# 1️⃣8️⃣ Global Explanation Report

A textual summary is generated as:

    results/stage6_explainability/
    └── Global_Explanation_Report.txt

The report records the extracted:

    Top 10 Features

and:

    Top 10 Attention Days

together with their corresponding values.

------------------------------------------------------------------------

# 1️⃣9️⃣ Local Explanation

### Script

    local_explanations.py

The local explanation module provides an example
participant/prediction-level interpretation.

The script uses:

    data/processed/rhrs_dataset.csv

and the TFT prediction results generated during Stage 5.

The feature-importance table generated by Stage 6 is also used. The
resulting local contribution representation is an interpretation aid
based on the observed feature values and TFT-derived global importance;
it is not a direct gradient-based decomposition of the TFT forward pass.

------------------------------------------------------------------------

# 2️⃣0️⃣ Local Prediction Example

The local explanation implementation selects an example prediction from
the TFT prediction results.

The selected prediction provides:

    Actual RHRS
    Predicted RHRS

The purpose is to demonstrate how the model's global feature information
can be used to construct a local explanation for an individual
prediction. The example is intended for model interpretation and is not
a participant-level clinical assessment or recommendation.

------------------------------------------------------------------------

# 2️⃣1️⃣ Local Feature Contributions

The selected features are combined with their corresponding importance
values.

The implementation calculates a contribution representation using the
feature value and importance information.

The resulting table contains:

    Feature
    Value
    Importance
    Contribution

------------------------------------------------------------------------

# 2️⃣2️⃣ Local Explanation Output

The local explanation table is stored as:

    results/stage6_explainability/
    └── Table_26_Local_Explanation.csv

The corresponding visualization is:

    results/stage6_explainability/
    └── Figure_15_Local_Explanation.png

A textual explanation is also generated:

    results/stage6_explainability/
    └── Local_Explanation_Report.txt

------------------------------------------------------------------------

# 2️⃣3️⃣ SHAP Analysis

### Script

    shap_analysis.py

The SHAP analysis provides an additional feature-attribution analysis.

The script loads the trained TFT checkpoint from:

    results/stage5_forecasting/checkpoints/tft_final.ckpt

and uses the RHRS dataset:

    data/processed/rhrs_dataset.csv

The feature representation contains:

    RHRS
    HRS
    PRS
    MRS
    BRS
    SRS
    lh
    estrogen
    pdg
    mean_rmssd
    mean_lf
    mean_hf
    mean_glucose
    std_glucose
    resting_hr
    sleep_score
    deep_sleep
    stress_score

------------------------------------------------------------------------

# 2️⃣4️⃣ SHAP Sampling

The current implementation creates:

    100 background observations

using:

    random_state = 42

and:

    50 explanation observations

using:

    random_state = 123

The SHAP computation uses:

    nsamples = 100

for the KernelExplainer evaluation.

------------------------------------------------------------------------

# 2️⃣5️⃣ SHAP Predictor Implementation

The current SHAP implementation constructs a surrogate predictor using
the feature-importance values generated by:

    Table_22_Feature_Importance.csv

The importance values are normalized to obtain feature weights.

The surrogate prediction is then calculated from the weighted feature
representation.

The resulting surrogate predictor is passed to:

    shap.KernelExplainer()

This implementation detail is important for reproducibility.

The current script therefore calculates SHAP values for the implemented
surrogate predictor constructed from the TFT feature-importance weights
rather than directly applying KernelSHAP to the original sequential TFT
forward pass. Accordingly, these SHAP values should be interpreted as
post-hoc attribution of the TFT-derived feature representation, not as a
direct SHAP decomposition of the original TFT forward pass.

------------------------------------------------------------------------

# 2️⃣6️⃣ SHAP Importance Calculation

Mean absolute SHAP values are calculated across the explanation samples.

The resulting table contains:

    Feature
    MeanAbsSHAP

and is sorted in descending order.

Output:

    results/stage6_explainability/
    └── Table_27_SHAP_Importance.csv

------------------------------------------------------------------------

# 2️⃣7️⃣ Manuscript SHAP Results

The manuscript reports the following SHAP values in Table VI:

  Feature        SHAP Value
  ------------ ------------
  mean lf             46.63
  mean hf             45.86
  mean rmssd           1.92
  estrogen             1.24
  BRS                  1.21
  MRS                  1.02
  PRS                  0.89
  SRS                  0.89
  resting hr           0.73
  HRS                  0.56

The manuscript reports low- and high-frequency HRV among the strongest
SHAP contributors.

------------------------------------------------------------------------

# 2️⃣8️⃣ SHAP Visualizations

The SHAP analysis produces:

    results/stage6_explainability/
    ├── Figure_16_SHAP_Barplot.png
    └── Figure_17_SHAP_Summary.png

### Figure 16

The SHAP bar plot presents mean absolute SHAP importance for the
analyzed features.

### Figure 17

The SHAP summary plot provides the distribution of SHAP contributions
across the explanation samples.

------------------------------------------------------------------------

# 2️⃣9️⃣ Explainability Across the Two Forecast Horizons

The overall WomenHealthAI forecasting study evaluates:

    H7
    H14

The explainability stage follows the same experimental configuration
principle.

For an H7 explainability run:

    14-day encoder window
    +
    HORIZON = 7
    +
    max_prediction_length = 7

For an H14 explainability run:

    14-day encoder window
    +
    HORIZON = 14
    +
    max_prediction_length = 14

The horizon is manually changed before the corresponding experiment is
executed. H7 and H14 explainability artifacts should be stored
separately and clearly labeled by horizon so that results from one
configuration are not confused with the other.

------------------------------------------------------------------------

# 3️⃣0️⃣ Recommended Reproduction Procedure

## Step 1 --- Complete Stage 5 H7 Experiment

Configure:

    HORIZON = 7

and:

    max_prediction_length = 7

Run the TFT forecasting experiment.

Preserve the generated H7 model/prediction artifacts.

------------------------------------------------------------------------

## Step 2 --- Run Stage 6 H7 Explainability

Execute the Stage 6 explainability scripts using the corresponding H7
TFT configuration.

Run:

    python feature_importance.py

    python attention_analysis.py

    python global_explanations.py

    python local_explanations.py

    python shap_analysis.py

------------------------------------------------------------------------

## Step 3 --- Complete Stage 5 H14 Experiment

Change the forecasting configuration to:

    HORIZON = 14

and:

    max_prediction_length = 14

Run the TFT forecasting experiment again.

Preserve the generated H14 model/prediction artifacts.

------------------------------------------------------------------------

## Step 4 --- Run Stage 6 H14 Explainability

Execute the Stage 6 explainability scripts using the corresponding H14
TFT configuration.

Run:

    python feature_importance.py

    python attention_analysis.py

    python global_explanations.py

    python local_explanations.py

    python shap_analysis.py

------------------------------------------------------------------------

# 3️⃣1️⃣ Important Horizon Reproducibility Note

The repository uses a manually configured forecasting horizon.

Therefore, users reproducing the experiments should not assume that a
single static value simultaneously represents both forecasting tasks.

The required procedure is:

    H7:
    HORIZON = 7
    max_prediction_length = 7

followed by:

    H14:
    HORIZON = 14
    max_prediction_length = 14

The historical encoder length remains:

    14 days

for both experiments.

This reproduces the multi-horizon experimental design used in the study.

------------------------------------------------------------------------

# 3️⃣2️⃣ Manuscript Forecasting Results

The manuscript reports the following TFT forecasting performance:

  Horizon       MAE    RMSE      R²   Pearson r
  --------- ------- ------- ------- -----------
  7-day       4.929   6.292   0.522       0.726
  14-day      5.342   6.834   0.449       0.679

These results demonstrate that the explainability analysis belongs to a
forecasting framework evaluated at both horizons.

------------------------------------------------------------------------

# 3️⃣3️⃣ Manuscript Explainability Results

The manuscript's explainability analysis reports:

### Feature Importance

The dominant reported features include:

    mean rmssd
    sleep score
    SRS
    MRS
    mean lf

### Temporal Attention

The attention analysis identifies recent historical observations
together with positions approximately one week earlier.

### SHAP

The strongest reported SHAP contributors include:

    mean lf
    mean hf
    mean rmssd

The manuscript combines these analyses to provide complementary
feature-level and temporal interpretations of the TFT forecasting
process.

------------------------------------------------------------------------

# 3️⃣4️⃣ Manuscript Figure Alignment

The manuscript presents the explainability analysis as:

    Figure 4

with three components:

    (a) TFT Feature Importance
    (b) Temporal Attention Weights
    (c) Global SHAP Importance

The figure is described as:

    Explainability analysis of the proposed TFT-based
    reproductive health resilience forecasting framework.

------------------------------------------------------------------------

# 3️⃣5️⃣ Manuscript Table Alignment

The explainability results are summarized in:

    TABLE VI:
    Summary of Explainability Analysis Results

The table contains three principal analysis groups:

  Analysis                 Information
  ------------------------ -------------------------------------
  TFT Feature Importance   Feature and importance
  Attention Analysis       Historical day and attention weight
  SHAP Analysis            Feature and SHAP value

The repository outputs provide the underlying computational artifacts
for these explainability analyses.

------------------------------------------------------------------------

# 3️⃣6️⃣ Complete Output Structure

The Stage 6 results directory contains:

    results/
    └── stage6_explainability/
        │
        ├── Table_22_Feature_Importance.csv
        ├── Table_23_Attention_Weights.csv
        ├── Table_24_Top10_Features.csv
        ├── Table_25_Top10_Attention_Days.csv
        ├── Table_26_Local_Explanation.csv
        ├── Table_27_SHAP_Importance.csv
        │
        ├── Figure_12_Feature_Importance.png
        ├── Figure_13_Attention_Weights.png
        ├── Figure_14_Global_Explanations.png
        ├── Figure_15_Local_Explanation.png
        ├── Figure_16_SHAP_Barplot.png
        ├── Figure_17_SHAP_Summary.png
        │
        ├── Global_Explanation_Report.txt
        └── Local_Explanation_Report.txt

------------------------------------------------------------------------

# 3️⃣7️⃣ Output-to-Script Mapping

  --------------------------------------------------------------------------
  Script                     Main Function           Primary Output
  -------------------------- ----------------------- -----------------------
  `feature_importance.py`    TFT feature importance  Table 22, Figure 12

  `attention_analysis.py`    Temporal attention      Table 23, Figure 13

  `global_explanations.py`   Global explanation      Tables 24--25, Figure
                                                     14

  `local_explanations.py`    Local explanation       Table 26, Figure 15

  `shap_analysis.py`         SHAP attribution        Table 27, Figures
                                                     16--17
  --------------------------------------------------------------------------

------------------------------------------------------------------------

# 3️⃣8️⃣ Reproducibility Map

    Stage 5 H7 TFT
          │
          ▼
    Stage 6 H7 Explainability
          │
          ├── Feature Importance
          ├── Temporal Attention
          ├── Global Explanation
          ├── Local Explanation
          └── SHAP
          
    Stage 5 H14 TFT
          │
          ▼
    Stage 6 H14 Explainability
          │
          ├── Feature Importance
          ├── Temporal Attention
          ├── Global Explanation
          ├── Local Explanation
          └── SHAP

The two branches use the same explainability methodology while
corresponding to their respective forecasting configurations.

------------------------------------------------------------------------

# 3️⃣9️⃣ Relationship to the Overall WomenHealthAI Framework

The complete framework follows:

    Multimodal Data Integration
              │
              ▼
            EDA
              │
              ▼
        RHRS Construction
              │
              ▼
        RHRS Validation
              │
              ▼
      Temporal Forecasting
              │
       ┌──────┴──────┐
       ▼             ▼
      H7            H14
       │             │
       └──────┬──────┘
              ▼
          TFT Model
              │
              ▼
       Explainability
              │
       ┌──────┼─────────┐
       ▼      ▼         ▼
    Feature Attention  SHAP
    Importance
       │      │         │
       └──────┼─────────┘
              ▼
      Global / Local
       Explanation
              │
              ▼
     Personalized Intervention
              │
              ▼
        LLM-Based Guidance

The manuscript describes WomenHealthAI as integrating RHRS formulation,
multi-horizon forecasting, explainability, personalized intervention,
and LLM-based guidance within one framework.

------------------------------------------------------------------------

# 4️⃣0️⃣ Important Implementation Notes

### 🔹 Two forecasting horizons

The study evaluates both:

    7-day forecasting

and:

    14-day forecasting

### 🔹 Fixed historical window

Both experiments use:

    14-day historical context

### 🔹 Manual horizon switching

The forecasting horizon is manually changed between runs.

### 🔹 No simultaneous H7/H14 training

H7 and H14 are treated as separate experimental configurations.

### 🔹 Stage 6 depends on Stage 5

The explainability scripts require the corresponding trained TFT
model/checkpoint and forecasting artifacts.

### 🔹 Explainability methods are complementary

Feature importance, temporal attention, global explanations, local
explanations, and SHAP are not identical measures.

They provide different views of model behavior.

### 🔹 SHAP implementation detail

The current SHAP script constructs a surrogate predictor from the TFT
feature-importance weights before applying KernelSHAP.

This implementation detail should be retained when reproducing the
repository results.

------------------------------------------------------------------------

# 4️⃣1️⃣ Interpretation Scope

The explainability results should be interpreted as **model
explanations**, not as independent clinical evidence.

Participant-level examples and individual prediction records used for
local explanations are analysis artifacts. They should not be
redistributed publicly unless release is explicitly authorized; public
releases should retain only approved aggregate or non-identifying
explainability outputs.

The feature-importance and attention analyses describe patterns learned
by the forecasting model.

The SHAP analysis describes feature attribution within the implemented
SHAP predictor.

These analyses therefore improve transparency into model behavior but do
not by themselves establish clinical causality, clinical validity, or
clinical usefulness.

------------------------------------------------------------------------

# 4️⃣2️⃣ Stage 6 Summary

Stage 6 provides the explainability layer of WomenHealthAI.

It supports the multi-horizon TFT forecasting experiments through:

    ✔ 7-day forecasting configuration
    ✔ 14-day forecasting configuration
    ✔ 14-day historical encoder window
    ✔ TFT feature importance
    ✔ Temporal attention analysis
    ✔ Global explanations
    ✔ Local explanations
    ✔ SHAP-based attribution
    ✔ Explainability tables
    ✔ Explainability figures
    ✔ Global explanation report
    ✔ Local explanation report

The resulting artifacts provide the computational evidence underlying
the explainability analysis reported in the manuscript, including the
feature-importance, temporal-attention, and SHAP results summarized in
Table VI and Figure 4.
