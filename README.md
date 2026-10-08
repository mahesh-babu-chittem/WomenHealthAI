# WomenHealthAI

## Multimodal Reproductive Health Intelligence Framework

WomenHealthAI is a unified multimodal framework for reproductive health resilience assessment, temporal forecasting, explainability, personalized intervention recommendation, and LLM-based health guidance.

The framework integrates longitudinal reproductive-health observations across hormonal, physiological, metabolic, behavioral, sleep, stress, glucose, and symptom-related domains to construct a Reproductive Health Resilience Score (RHRS). The resulting RHRS is validated, forecast over multiple temporal horizons, interpreted using explainability methods, converted into intervention priorities, and communicated through locally executed LLM-based reports.

The repository is organized as a sequence of reproducible computational stages corresponding to the methodology and experimental analysis reported in the WomenHealthAI manuscript.

---

# 📌 Framework Overview

The complete WomenHealthAI workflow is:

```text
Multimodal Participant Observations
                │
                ▼
┌───────────────────────────────┐
│ Stage 1                       │
│ Data Integration & Preparation│
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Stage 2                       │
│ Exploratory Data Analysis     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Stage 3                       │
│ RHRS Construction             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Stage 4                       │
│ RHRS Validation               │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Stage 5                       │
│ Temporal Forecasting          │
│ H7 / H14                      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Stage 6                       │
│ Explainability                │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Stage 7                       │
│ Personalized Intervention     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Stage 8                       │
│ LLM-Based Guidance            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Stage 9                       │
│ Ablation Analysis             │
└───────────────────────────────┘
```

Each stage has its own README describing the implementation, inputs,
outputs, execution procedure, and reproducibility information.

---

# 📂 Repository Structure

```text
project/
│
├── README.md
│
├── stage1_data_integration/
│   ├── scripts/
│   └── README.md
│
├── stage2_eda/
│   ├── scripts/
│   └── README.md
│
├── stage3_rhrs/
│   ├── scripts/
│   └── README.md
│
├── stage4_validation/
│   ├── scripts/
│   └── README.md
│
├── stage5_forecasting/
│   ├── scripts/
│   └── README.md
│
├── stage6_explainability/
│   ├── scripts/
│   └── README.md
│
├── stage7_intervention/
│   ├── scripts/
│   └── README.md
│
├── stage8_llm/
│   ├── scripts/
│   └── README.md
│
├── stage9_ablation/
│   ├── scripts/
│   └── README.md
│
├── data/
│
└── results/
    ├── stage1_data_integration/
    ├── stage2_eda/
    ├── stage3_rhrs/
    ├── stage4_validation/
    ├── stage5_forecasting/
    ├── stage6_explainability/
    ├── stage7_intervention/
    ├── stage8_llm/
    └── stage9_ablation/
```

The `results/` directory is a repository-level output directory. It is not
nested inside the individual stage directories.

---

# 🔬 Stage Descriptions

## Stage 1 — Data Integration and Preparation

Stage 1 integrates the available multimodal reproductive-health
observations into a unified participant-day representation.

The integration includes measurements from domains such as:

- Hormonal measurements
- Heart-rate variability
- Resting heart rate
- Glucose
- Sleep
- Stress
- Symptoms
- Other longitudinal reproductive-health variables

The stage performs data organization, integration, missing-value handling,
and preparation of the RHRS-enriched dataset used by subsequent stages.

Detailed implementation information is provided in:

```text
stage1_data_integration/README.md
```

The resulting processed data are used as input to the downstream RHRS,
forecasting, explainability, intervention, and LLM stages.

The median harmonization performed at this stage is part of the cohort-level
construction of the unified multimodal participant-day representation. It
establishes the common analytical representation used by subsequent stages;
additional model-specific data-dependent preprocessing is handled within the
corresponding forecasting workflow.

---

# 📊 Stage 2 — Exploratory Data Analysis

Stage 2 performs exploratory analysis of the integrated multimodal dataset.

The analysis examines:

- Distributional characteristics
- Missingness
- Relationships between variables
- Correlation structure
- RHRS-related feature relationships
- Participant-level and temporal characteristics

The stage produces aggregate exploratory results and figures used to
support the methodological analysis.

Detailed procedures are documented in:

```text
stage2_eda/README.md
```

---

# 🧮 Stage 3 — RHRS Construction

Stage 3 constructs the Reproductive Health Resilience Score (RHRS).

The framework defines five resilience dimensions:

```text
HRS — Hormonal Resilience Score
PRS — Physiological Resilience Score
MRS — Metabolic Resilience Score
BRS — Behavioral Resilience Score
SRS — Symptom/Stress Resilience Score
```

The overall RHRS is calculated using the weighted formulation:

\[
RHRS =
0.25HRS +
0.25PRS +
0.15MRS +
0.20BRS +
0.15SRS
\]

The resulting score is constrained to the defined RHRS range.

The stage also documents:

- Component construction
- Normalization
- Weighting
- Score direction
- Menstrual-phase interpretation
- Fictional worked examples
- Participant-day interpretation

The percentile transformation used for RHRS is part of the RHRS definition
and establishes a common analytical scale across the heterogeneous
measurements; it is not a trainable parameter of the downstream forecasting
models.

A fictional worked example is included in the Stage 3 documentation to
demonstrate how individual component values are transformed into the
overall RHRS.

The fictional example is not derived from an actual participant record.

Detailed implementation:

```text
stage3_rhrs/README.md
```

---

# 📐 Stage 4 — RHRS Validation

Stage 4 evaluates the reliability and validity of the proposed RHRS.

The validation includes:

- Internal consistency
- Convergent validity
- Known-group analysis where applicable
- Predictive validity
- Correlation analysis
- Statistical characterization

Internal consistency is evaluated using Cronbach's alpha. The validated
Stage 4 result is α = 0.163. This indicates limited internal consistency
among the five dimensions and is interpreted cautiously because RHRS is a
multidimensional composite whose dimensions represent distinct
physiological, reproductive, metabolic, behavioral, and symptom-related
domains rather than interchangeable measures of one latent construct.

For the five RHRS dimensions:

\[
\alpha =
\frac{k}{k-1}
\left(
1 -
\frac{\sum_{i=1}^{k}\sigma_i^2}
{\sigma_t^2}
\right)
\]

where \(k=5\).

The stage also reports correlations between RHRS and selected physiological,
hormonal, sleep, and stress-related variables.

Correlation is interpreted as an association measure and is not treated as
evidence of causality.

Detailed validation procedures and outputs are documented in:

```text
stage4_validation/README.md
```

---

# 🔭 Stage 5 — Temporal RHRS Forecasting

Stage 5 implements the temporal forecasting component of WomenHealthAI.

The forecasting framework uses a fixed:

```text
Historical window = 14 days
```

The canonical TFT workflow uses the same chronological 70%/15%/15%
train/validation/test split for H7 and H14. The final decoder-step prediction
is used for the requested forecast horizon, and the prediction count is
checked against the corresponding canonical test metadata.

and evaluates two forecasting horizons:

```text
H7  = 7-day forecasting
H14 = 14-day forecasting
```

The model suite includes:

```text
Linear Regression
Random Forest
XGBoost
LSTM
GRU
BiLSTM
Temporal Transformer
Temporal Fusion Transformer
```

Detailed implementation and experimental configuration are documented in:

```text
stage5_forecasting/README.md
```

---

# 🔭 H7 and H14 Temporal Forecasting Procedure

The temporal-window construction uses the same 14-day historical context for
both forecasting horizons.

For a concrete illustrative example, assume that a participant has
consecutive daily observations from 1 January through 28 January.

The example below is entirely fictional and is included only to explain the
temporal-window construction.

## H7 Example

The first historical window consists of:

```text
1 January – 14 January
```

These 14 observations form the input sequence.

The forecasting horizon is:

```text
HORIZON = 7
```

The final historical observation occurs on 14 January.

Therefore:

```text
14 January + 7 days = 21 January
```

The resulting forecasting sample is:

```text
Input:
Observations from 1 January – 14 January

Target:
RHRS on 21 January
```

Conceptually:

```text
1 Jan ───────────────── 14 Jan ─────────────── 21 Jan
     14-day history          7-day horizon
                                  │
                                  ▼
                            Target RHRS
```

Therefore:

```text
1 January – 14 January → 21 January
14-day historical input → 7-day-ahead RHRS target
```

## H14 Example

The same historical window is used:

```text
1 January – 14 January
```

The forecasting horizon is changed to:

```text
HORIZON = 14
```

Therefore:

```text
14 January + 14 days = 28 January
```

The resulting forecasting sample is:

```text
Input:
Observations from 1 January – 14 January

Target:
RHRS on 28 January
```

Conceptually:

```text
1 Jan ───────────────── 14 Jan ───────────────────────── 28 Jan
     14-day history                14-day horizon
                                           │
                                           ▼
                                     Target RHRS
```

Therefore:

```text
1 January – 14 January → 28 January
14-day historical input → 14-day-ahead RHRS target
```

## Subsequent Windows

The same procedure is shifted chronologically across the participant's
available observations.

For example:

```text
Window 1:
1 Jan – 14 Jan → 21 Jan  (H7)
1 Jan – 14 Jan → 28 Jan  (H14)

Window 2:
2 Jan – 15 Jan → 22 Jan  (H7)
2 Jan – 15 Jan → 29 Jan  (H14)

Window 3:
3 Jan – 16 Jan → 23 Jan  (H7)
3 Jan – 16 Jan → 30 Jan  (H14)

...
```

Thus, every forecasting sample contains:

```text
14 consecutive historical observations
                │
                ▼
       Temporal input sequence
                │
                ▼
        Forecasting model
                │
                ▼
        Future RHRS target
```

The procedure is repeated for each valid chronological window and for each
participant.

The dates above are fictional and do not represent an actual participant
record.

---

# 📏 Forecasting Evaluation

All forecasting models are evaluated using a common evaluation framework.

The evaluation includes:

```text
MAE
MSE
RMSE
MAPE
SMAPE
Median Absolute Error
Maximum Error
R²
Explained Variance
Pearson Correlation
Spearman Correlation
Kendall's Tau
Trend Accuracy
Trend Precision
Trend Recall
Trend F1
Risk Classification Metrics
ROC-AUC
PR-AUC
Cohen's d
Statistical Significance
```

---

# 📐 RMSE and R² Calculation

RMSE and R² are calculated independently from the same ground-truth
(`y_true`) and prediction (`y_pred`) arrays for each evaluation run.

RMSE is calculated as:

\[
RMSE =
\sqrt{
\frac{1}{n}
\sum_{i=1}^{n}
(y_i-\hat{y}_i)^2
}
\]

R² is calculated as:

\[
R^2 =
1 -
\frac{
\sum_{i=1}^{n}
(y_i-\hat{y}_i)^2
}{
\sum_{i=1}^{n}
(y_i-\bar{y})^2
}
\]

RMSE measures the magnitude of prediction error in the same numerical
units as RHRS.

R² measures the proportion of variance in the observed RHRS values
accounted for by the predictions relative to a mean-based reference.

Consequently, RMSE and R² do not have a direct numerical correspondence.
A particular RMSE value does not imply a fixed R² value because R² also
depends on the variance of the ground-truth values in the evaluation set.

Both metrics are computed from the same `y_true` and `y_pred` arrays by
the shared regression-metric implementation.

---

# 🧪 Forecasting Data Split

The forecasting experiments use a chronological:

```text
70% Training
15% Validation
15% Testing
```

split.

Temporal ordering is retained to prevent future observations from being
randomly mixed into earlier partitions.

The test partition is reserved for final model evaluation.

Detailed split configuration and implementation are documented in:

```text
stage5_forecasting/README.md
```

---

# 🧠 Stage 6 — Explainability

Stage 6 provides model interpretability for the temporal forecasting
component.

The explainability analysis includes:

```text
TFT feature importance
Temporal attention analysis
SHAP-based global importance
```

TFT feature importance and temporal attention are obtained from the trained
TFT. The SHAP analysis is a post-hoc attribution of the TFT-derived feature
representation through a weighted surrogate model; it is not a direct SHAP
decomposition of the original TFT forward pass.

The explainability outputs are generated from the trained forecasting
models and corresponding prediction data.

Detailed procedures are documented in:

```text
stage6_explainability/README.md
```

---

# 🎯 Stage 7 — Personalized Intervention

Stage 7 converts the RHRS resilience profile into intervention priorities.

For each resilience dimension:

```text
HRS
PRS
MRS
BRS
SRS
```

an intervention priority can be derived from the corresponding resilience
value.

The priority formulation used in the manuscript is:

\[
P_i = 100-R_i
\]

where:

```text
Ri ∈ {HRS, PRS, MRS, BRS, SRS}
```

The resulting priorities are used to identify dimensions requiring greater
attention within the framework.

The recommendations are generated from the individual's latest observed
RHRS profile rather than treating a future forecast as an already observed
clinical state. The intervention module is therefore treated as a
research-prototype decision-support component rather than a clinical
diagnostic or treatment system.

Detailed implementation:

```text
stage7_intervention/README.md
```

---

# 🤖 Stage 8 — LLM-Based Guidance

Stage 8 provides a communication layer for converting structured RHRS,
risk, and intervention information into readable reproductive-health
reports.

The implementation uses a locally executed Llama-3 model through Ollama.

The current repository documentation identifies the model as:

```text
llama3:latest
```

The LLM receives structured information from the Stage 7 intervention
output rather than independently processing the raw multimodal dataset. The
Stage 8 input contains the current RHRS profile, risk category, and
intervention recommendations.

The report-generation workflow is:

```text
Observed RHRS Profile
      │
      ▼
Risk Category
      │
      ▼
Intervention Priorities
      │
      ▼
Local Llama-3
      │
      ▼
Generated Report
```

The LLM is not the forecasting engine, RHRS calculator, or explainability
engine.

It is used to communicate structured analytical results.

---

# 📝 LLM Prompt and Input Handling

The Stage 8 prompts provide structured information including the RHRS
profile, risk category, and intervention recommendations.

The generation constraints include:

```text
Maximum 250 words
No diagnosis
Health-oriented explanatory language
Recommendation concepts derived from the intervention stage
```

The exact prompt templates and execution details are documented in:

```text
stage8_llm/README.md
```

The repository should preserve the exact prompt template used for the
reported experiments.

Any future modification to the prompt should be treated as a separate
experimental configuration.

---

# 📊 Guidance Fidelity Score

Generated reports are evaluated using the Guidance Fidelity Score (GFS).

The implementation uses:

\[
GFS =
\frac{|C|}{|T|}
\]

where:

```text
C = number of expected intervention concepts covered
T = total expected intervention concepts
```

The reported Stage 8 aggregate result is:

```text
Mean GFS = 1.000
```

Other reported aggregate measures include:

```text
Mean Word Count = 230.88
Mean Readability Score = 13.35
```

GFS measures coverage of predefined intervention concepts.

A high GFS does not establish:

```text
Clinical correctness
Clinical safety
Factual correctness
Appropriateness
Absence of hallucinations
Clinical usefulness
Patient satisfaction
```

Therefore, GFS should be interpreted as a communication/coverage measure
rather than a clinical validation metric.

---

# 🔐 Data Access and Privacy

The underlying **mcPHASES participant-level data are restricted study
data and are not publicly available for unrestricted download**.

Researchers reproducing the participant-level analyses must obtain
authorized access to mcPHASES through the applicable dataset access process
and comply with its data-use and ethics requirements.

The public repository does not redistribute:

```text
Raw participant records
Merged participant-level datasets
Individual RHRS trajectories
Individual predictions
Participant-specific reports
Restricted intermediate datasets
```

The public repository contains:

```text
Source code
Configuration files
Documentation
Aggregate results
Figures derived from aggregate analyses
Clearly identified fictional examples
```

Researchers seeking to reproduce the participant-level analyses should
first obtain authorized access to the mcPHASES dataset through the
applicable mcPHASES data-access process.

After authorized access is obtained, the data should be stored locally
according to the directory structure expected by the Stage 1 processing
pipeline. Participant-level data must remain within the authorized research
environment and must not be redistributed through the public repository.

---

# 🧪 Fictional Examples and Study Results

Fictional examples are used only where a concrete numerical or temporal
example is required to explain the implementation.

Examples include:

```text
RHRS worked examples
Temporal forecasting date examples
Input/target forecasting demonstrations
LLM recommendation traces
```

All such examples are explicitly labelled as fictional or illustrative.

They must not be interpreted as participant-level study results.

Conversely, numerical results reported from the experiments, including
forecasting metrics, validation statistics, ablation results, and LLM
aggregate results, correspond to the study analysis and are not generated
from the fictional examples.

---

# 🛡️ Participant-Level Data Protection

Before committing changes to the repository, participant-level information
must be excluded from public files.

Particular attention should be given to:

```text
CSV files
JSON files
Prediction files
Generated reports
Notebook outputs
Training logs
Debug logs
Screenshots
Figures
Temporary files
Model-analysis artifacts
```

Participant identifiers and other potentially identifying information
should not be committed unless explicitly permitted under the applicable
data-access and governance requirements.

---

# 🧠 LLM Data Handling

The LLM stage is designed around local model execution through Ollama.

The intended data flow is:

```text
Restricted mcPHASES study data
        │
        ▼
WomenHealthAI processing
        │
        ▼
Structured analytical outputs
        │
        ▼
Local Llama-3 execution
        │
        ▼
Generated report
```

The repository does not require uploading participant-level study data to
a third-party hosted LLM API.

The exact local model identifier, prompt template, runtime, and generation
parameters explicitly passed by the implementation should be recorded for
reproducibility. The current Stage 8 implementation uses `llama3:latest`
through Ollama and does not explicitly pass temperature, top-p, seed, or a
token-limit parameter.

The public repository should contain only fictional report examples or
aggregate report-quality results.

Participant-specific generated reports should remain outside the public
repository unless their release is explicitly authorized.

---

# ⚖️ Ethics and Responsible Use

WomenHealthAI is a research decision-support framework and should not be
interpreted as an autonomous clinical diagnostic or treatment system.

The repository is intended to support reproducibility of the research
computational pipeline.

Use of restricted mcPHASES data requires appropriate authorization through
the data provider's access procedures.

Any researcher reproducing the study is responsible for complying with:

```text
Applicable data-use agreements
Institutional requirements
Dataset access conditions
Privacy requirements
Ethical approval or exemption requirements
Local research governance
```

The repository does not provide permission to redistribute restricted
participant data.

The exact institutional ethics approval or exemption information applicable
to the study should be retained in the manuscript and study documentation
and should not be inferred from the repository.

---

# 🔄 Reproducibility Principles

The repository follows the following reproducibility principles.

## 1. Stage-wise Execution

Each stage has its own implementation and README.

```text
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5
                                      ↓
Stage 9 ← Stage 8 ← Stage 7 ← Stage 6
```

## 2. Restricted Data Separation

Study data remain outside the public repository.

## 3. Fictional Examples

Illustrative examples are clearly labelled.

## 4. Aggregate Results

Published repository results are provided at aggregate level where
participant-level release is restricted.

## 5. Script-to-Result Traceability

Each major experimental result is associated with the corresponding
implementation stage and output directory.

## 6. Manuscript Alignment

The repository is structured to correspond to the methodological and
experimental components reported in the manuscript.

---

# 📁 Results Organization

All stage outputs are organized under:

```text
results/
```

with one subdirectory per stage:

```text
results/
├── stage1_data_integration/
├── stage2_eda/
├── stage3_rhrs/
├── stage4_validation/
├── stage5_forecasting/
├── stage6_explainability/
├── stage7_intervention/
├── stage8_llm/
└── stage9_ablation/
```

This separation keeps source code and generated outputs distinct.

---

# 📈 Major Reported Results

The manuscript reports TFT forecasting results for both horizons.

| Horizon | MAE | RMSE | R² | Pearson r |
|---|---:|---:|---:|---:|
| 7-day | 4.929 | 6.292 | 0.522 | 0.726 |
| 14-day | 5.342 | 6.834 | 0.449 | 0.679 |

The reported 7-day model comparison includes:

| Model | MAE | RMSE | R² | Pearson r |
|---|---:|---:|---:|---:|
| Linear Regression | 6.656 | 8.305 | 0.345 | 0.600 |
| Random Forest | 6.448 | 8.084 | 0.380 | 0.628 |
| XGBoost | 6.654 | 8.238 | 0.356 | 0.602 |
| LSTM | 6.692 | 8.391 | 0.332 | 0.598 |
| GRU | 7.160 | 8.811 | 0.263 | 0.516 |
| BiLSTM | 7.341 | 9.037 | 0.225 | 0.562 |
| Temporal Transformer | 7.141 | 8.917 | 0.245 | 0.572 |
| Temporal Fusion Transformer | 4.929 | 6.292 | 0.522 | 0.726 |

These values correspond to the study experiments and should not be
recalculated from fictional examples.

---

# 🧪 Ablation Analysis

Stage 9 evaluates the contribution of individual framework components.

The ablation analysis includes:

```text
Full WomenHealthAI
w/o HRS
w/o PRS
w/o MRS
w/o BRS
w/o SRS
Equal-weight RHRS
w/o Temporal Attention
w/o Adaptive Variable Selection
```

The reported results cover both:

```text
7-day forecasting
14-day forecasting
```

The Stage 9 implementation and output tables document the calculations
underlying the reported ablation results.

The ablation analysis distinguishes RHRS-dimension input-removal
experiments, the equal-weight RHRS target-weighting analysis, and
architectural component ablations. The detailed Stage 9 README documents
the specific experimental implementation and aggregate results.

Detailed implementation:

```text
stage9_ablation/README.md
```

---

# 🔬 Reproducibility of Validation and Ablation Results

The repository is designed so that the calculations supporting the
manuscript tables and figures can be traced to the relevant stage scripts.

The corresponding workflow is:

```text
Study Dataset
     │
     ▼
Stage 1
Data Preparation
     │
     ▼
Stage 2
EDA
     │
     ▼
Stage 3
RHRS
     │
     ▼
Stage 4
Validation
     │
     ├──────────────► Validation Results
     │
     ▼
Stage 5
Forecasting
     │
     ├──────────────► Forecasting Results
     │
     ▼
Stage 6
Explainability
     │
     ▼
Stage 7
Intervention
     │
     ▼
Stage 8
LLM Reports
     │
     ▼
Stage 9
Ablation
```

---

# 💻 Software Environment

The exact software environment should be installed according to the
requirements specified by the individual stage.

The project uses Python-based scientific computing and machine-learning
libraries.

The computational environment includes libraries and frameworks such as:

```text
Python
NumPy
Pandas
SciPy
scikit-learn
PyTorch
PyTorch Forecasting
XGBoost
SHAP
Matplotlib
textstat
Ollama
```

The exact versions required for each stage should be taken from the
corresponding stage requirements files.

The recorded project environment includes Python 3.12.2 and pandas 2.2.2.
Other historical dependency versions are not claimed unless they are
explicitly preserved in the repository.

For a new reproduction run, record the complete active environment with:

```bash
python --version
python -m pip --version
python -m pip freeze > environment_reproduction_freeze.txt
ollama --version
ollama list
python -c "import ollama; print(getattr(ollama, '__version__', 'version not exposed'))"
```

The Stage 8 LLM implementation uses the exact model identifier
`llama3:latest` through the Ollama `ollama.chat()` interface. No explicit
`temperature`, `top_p`, `seed`, or token-limit parameter is passed by the
implementation; the prompt-level 250-word instruction should not be
interpreted as an explicit generation token limit.

---

# 🛠️ Project-Wide Reproduction Commands

The complete reproduction should be performed only after authorized access
to the mcPHASES dataset has been obtained.

The stage-specific working commands are documented in each stage README.
The overall execution order is:

```bash
# Stage 1
python stage1_data_integration/merge_data.py
python stage1_data_integration/clean_data.py

# Stage 2
python stage2_eda/descriptive_statistics.py
python stage2_eda/missing_value_analysis.py
python stage2_eda/missing_feature_breakdown.py
python stage2_eda/correlation_analysis.py

# Stage 3
python stage3_rhrs/hormonal_resilience.py
python stage3_rhrs/physiological_resilience.py
python stage3_rhrs/metabolic_resilience.py
python stage3_rhrs/behavioral_resilience.py
python stage3_rhrs/symptom_resilience.py
python stage3_rhrs/compute_rhrs.py
python stage3_rhrs/rhrs_diagnostics.py

# Stage 4
python stage4_validation/reliability_analysis.py
python stage4_validation/convergent_validity.py
python stage4_validation/known_group_analysis.py
python stage4_validation/predictive_validity.py
python stage4_validation/validation_summary.py
```

Stage 5 is configured separately for H7 and H14 using the canonical
forecasting workflow documented in `stage5_forecasting/README.md`.

Stage 6, Stage 7, Stage 8, and Stage 9 are then executed using their
corresponding stage-specific README instructions. In particular, Stage 8
uses:

```bash
python ollama_guidance_generator.py
python llm_evaluation.py
```

The participant-level outputs generated during reproduction must remain in
the authorized research environment.


---

# 🚀 General Reproduction Workflow

## Step 1 — Obtain Authorized Data Access

Obtain authorized access to the mcPHASES study dataset through the
applicable mcPHASES data-access process. The dataset is not publicly
available for unrestricted download.

Do not place restricted participant-level data into the public repository.

## Step 2 — Configure the Local Dataset

Place the authorized dataset locally according to the input structure
specified by Stage 1.

## Step 3 — Run Data Integration

Execute the Stage 1 scripts.

```text
stage1_data_integration/
```

## Step 4 — Run Exploratory Analysis

Execute the Stage 2 scripts.

```text
stage2_eda/
```

## Step 5 — Construct RHRS

Execute the Stage 3 scripts.

```text
stage3_rhrs/
```

## Step 6 — Validate RHRS

Execute the Stage 4 validation pipeline.

```text
stage4_validation/
```

## Step 7 — Generate Forecasting Windows

Execute Stage 5 temporal-window generation.

```text
stage5_forecasting/
```

The forecasting configuration is evaluated separately for:

```text
HORIZON = 7
HORIZON = 14
```

## Step 8 — Train and Evaluate Forecasting Models

Run the Stage 5 model implementations and evaluation scripts.

The resulting metrics are stored under:

```text
results/stage5_forecasting/
```

## Step 9 — Run Explainability

Execute Stage 6.

```text
stage6_explainability/
```

## Step 10 — Generate Intervention Priorities

Execute Stage 7.

```text
stage7_intervention/
```

## Step 11 — Generate LLM-Based Reports

Run Stage 8 using the documented local Ollama/Llama-3 configuration.

```text
stage8_llm/
```

## Step 12 — Run Ablation Experiments

Execute Stage 9.

```text
stage9_ablation/
```

---

# 🗂️ Stage-to-Output Mapping

| Stage | Main Function | Output Location |
|---|---|---|
| Stage 1 | Data integration | `results/stage1_data_integration/` |
| Stage 2 | Exploratory analysis | `results/stage2_eda/` |
| Stage 3 | RHRS construction | `results/stage3_rhrs/` |
| Stage 4 | RHRS validation | `results/stage4_validation/` |
| Stage 5 | Temporal forecasting | `results/stage5_forecasting/` |
| Stage 6 | Explainability | `results/stage6_explainability/` |
| Stage 7 | Intervention | `results/stage7_intervention/` |
| Stage 8 | LLM guidance | `results/stage8_llm/` |
| Stage 9 | Ablation | `results/stage9_ablation/` |

---

# 📚 Manuscript Alignment

The repository corresponds to the methodological components of the
WomenHealthAI manuscript.

The major methodological sequence is:

```text
Multimodal Data Integration
        ↓
RHRS Formulation
        ↓
RHRS Validation
        ↓
Multi-Horizon Forecasting
        ↓
Explainability
        ↓
Personalized Intervention
        ↓
LLM-Based Guidance
        ↓
Ablation Analysis
```

The repository therefore provides the computational implementation
associated with the principal methodology and reported experiments.

---

# 🔎 Reviewer Reproducibility Clarifications

The repository explicitly addresses the following reproducibility points.

## Temporal Forecasting Clarification

The forecasting README provides a concrete step-by-step example showing how
a 14-day historical input window is converted into:

```text
1 January – 14 January → 21 January
```

for H7 and:

```text
1 January – 14 January → 28 January
```

for H14.

It also demonstrates how subsequent windows are shifted chronologically.

The dates are fictional and are used solely to explain the temporal-window
construction.

## Metric Calculation Clarification

The forecasting README documents the equations and implementation logic for
RMSE and R².

Both metrics are calculated from the same `y_true` and `y_pred` arrays.

RMSE quantifies prediction-error magnitude, whereas R² measures explained
variance relative to the mean-based reference.

Therefore, the two values are not expected to exhibit a direct numerical
correspondence.

---

# 🔒 What Is and Is Not Public

## Public Repository

The repository contains:

```text
Code
Documentation
Configuration
Aggregate experimental results
Aggregate figures
Fictional worked examples
Fictional temporal forecasting examples
```

## Restricted

The following should remain outside the public repository:

```text
Raw mcPHASES participant data
Merged participant-level datasets
Participant-level RHRS values
Participant-level forecasts
Participant-level recommendation reports
Restricted intermediate datasets
Unauthorized model outputs containing participant information
```

This separation is required to preserve participant privacy and comply with
the applicable study-data access conditions.

---

# 📝 Submitted Results and Subsequent Corrections

The repository distinguishes the artifacts corresponding to the submitted
manuscript results from subsequent corrected or clarified repository
artifacts.

In particular, the current documentation records the corrected Stage 4
reliability value (α = 0.163), corrected horizon-specific Stage 5 TFT
artifacts, clarified Stage 6 explainability interpretation, strengthened
Stage 7 research-prototype/safety wording, and the documented Stage 9
ablation distinctions. These corrections should not be interpreted as
additional historical experimental runs unless explicitly identified as
such in the corresponding stage documentation.

---

# 🧾 Reproducibility Checklist

Before considering a reproduction complete, verify:

```text
☐ Authorized dataset access obtained
☐ Dataset stored locally
☐ Stage 1 preprocessing completed
☐ Stage 2 EDA reproduced
☐ RHRS construction reproduced
☐ RHRS validation reproduced
☐ H7 temporal windows generated
☐ H14 temporal windows generated
☐ H7 models trained/evaluated
☐ H14 models trained/evaluated
☐ RMSE calculated from y_true/y_pred
☐ R² calculated from y_true/y_pred
☐ Explainability analysis reproduced
☐ Intervention analysis reproduced
☐ Local Llama-3 environment configured
☐ LLM prompts matched to documented version
☐ Aggregate report metrics reproduced
☐ Ablation experiments reproduced
☐ Generated files inspected for sensitive information
☐ No restricted participant-level files committed
```

---

# ⚠️ Important Interpretation Note

WomenHealthAI is a research framework for computational reproductive-health
resilience assessment and decision support.

The RHRS, forecasting outputs, explainability results, intervention
priorities, and generated LLM reports should not be interpreted as
independent clinical diagnoses or definitive medical recommendations.

In particular:

```text
Forecasting ≠ clinical diagnosis
Explainability ≠ causal inference
Intervention priority ≠ clinical treatment decision
GFS ≠ clinical correctness
LLM report quality ≠ clinical usefulness
```

The framework is intended to support research and structured
decision-support analysis.

---

# 📌 Citation

If this repository or the WomenHealthAI framework is used in academic
research, please cite the corresponding WomenHealthAI manuscript.

```text
WomenHealthAI:
A Multimodal Framework for Reproductive Health Resilience Assessment,
Temporal Forecasting, Explainability, Personalized Intervention
Recommendation, and LLM-Based Health Guidance.
```

The final bibliographic citation should be updated with the publication
venue, DOI, and repository URL when the publication record is finalized.

---

# 📄 License

Add the applicable repository license here before public release.

```text
License: [Specify applicable license]
```

The license does not override restrictions imposed by the underlying
mcPHASES study-data access conditions.

---

# 👥 Repository Organization

The repository separates:

```text
Methodology
Code
Results
Data Access
Documentation
```

The root README provides the overall framework and reproducibility
information, while each stage README provides the implementation-level
details for its corresponding computational component.

The repository therefore provides a traceable path from authorized
study-data access through preprocessing, RHRS construction, validation,
forecasting, explainability, intervention analysis, LLM communication,
and ablation experiments.

---

# 🔬 WomenHealthAI Research Pipeline Summary

```text
Authorized mcPHASES Dataset
            │
            ▼
    Data Integration
            │
            ▼
      Exploratory Analysis
            │
            ▼
       RHRS Construction
            │
            ▼
        RHRS Validation
            │
            ▼
    ┌───────┴────────┐
    │                │
   H7               H14
    │                │
    ▼                ▼
7-day Forecast   14-day Forecast
    │                │
    └───────┬────────┘
            │
            ▼
      Explainability
            │
            ▼
 Personalized Intervention
            │
            ▼
      Local Llama-3
            │
            ▼
   LLM-Based Guidance
            │
            ▼
      Ablation Analysis
            │
            ▼
     Aggregate Results
```

The complete computational evidence underlying the WomenHealthAI framework
is organized across the nine stage-specific implementations and their
corresponding result directories.
