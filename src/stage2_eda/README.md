# 📊 Stage 2 --- Exploratory Data Analysis

> **Purpose:** Characterize the integrated reproductive-health dataset,
> quantify feature-level statistics and missingness, and examine
> relationships among numerical variables before RHRS construction and
> temporal forecasting.

Stage 2 operates on the cleaned participant-day dataset produced by
**Stage 1 --- Data Integration & Preprocessing**.

The analysis provides the descriptive and correlation-based evidence
used to understand the structure of the multimodal dataset before the
downstream RHRS, validation, and forecasting stages.

------------------------------------------------------------------------

## 📌 Stage Overview

  ---------------------------------------------------------------------------------------------------
  Script                           Analysis                Main Output
  -------------------------------- ----------------------- ------------------------------------------
  `descriptive_statistics.py`      Dataset characteristics `Table_1_Dataset_Characteristics.csv`,
                                   and numerical feature   `Table_2_Feature_Statistics.csv`
                                   statistics              

  `missing_value_analysis.py`      Overall missing-value   `missing_value_report.csv`,
                                   assessment              `missing_value_report.json`

  `missing_feature_breakdown.py`   Feature-level           `Table_4_Missing_Feature_Breakdown.csv`,
                                   missing-value breakdown `missing_feature_breakdown.json`

  `correlation_analysis.py`        Pearson correlation     `Table_3_Correlation_Matrix.csv`,
                                   analysis and            `Figure_1_Correlation_Heatmap.png`
                                   visualization           
  ---------------------------------------------------------------------------------------------------

All scripts operate on:

`data/processed/clean_master_dataframe.csv`

and save their results under:

`results/stage2_eda/`

------------------------------------------------------------------------

## 🔎 1. Dataset Characteristics

### `descriptive_statistics.py`

The dataset characteristics script establishes the basic structure of
the processed dataset.

The following quantities are computed:

  -----------------------------------------------------------------------
  Quantity                            Description
  ----------------------------------- -----------------------------------
  👥 Participants                     Number of unique participant
                                      identifiers

  📄 Total rows                       Number of participant-day
                                      observations

  🧮 Total columns                    Number of columns in the processed
                                      dataframe

  📊 Total features                   Number of columns treated as
                                      analytical features by the script
  -----------------------------------------------------------------------

The implementation obtains the participant count from the unique `id`
values and derives the row and column counts directly from the loaded
dataframe.

The resulting dataset characteristics are saved as both JSON and CSV
outputs.

### Generated files

-   `descriptive_statistics.json`
-   `Table_1_Dataset_Characteristics.csv`

------------------------------------------------------------------------

## 📈 2. Numerical Feature Statistics

The same script extracts all numerical columns from the processed
dataframe and calculates descriptive statistics.

For each numerical feature, the generated statistics include:

  Statistic   Description
  ----------- ----------------------------------
  `count`     Number of available observations
  `mean`      Arithmetic mean
  `std`       Standard deviation
  `min`       Minimum value
  `25%`       First quartile
  `50%`       Median
  `75%`       Third quartile
  `max`       Maximum value

The median is explicitly calculated and added to the resulting
feature-statistics table. **This median is reported as a descriptive
statistic for characterizing the processed dataset; it is not used as a
model-training parameter or fitted preprocessing value.**

### Generated file

`Table_2_Feature_Statistics.csv`

This output provides the numerical basis for examining the distribution
and scale of the variables entering the subsequent analytical stages.

------------------------------------------------------------------------

## 🧩 3. Missing-Value Analysis

Stage 2 includes two complementary missing-value analyses.

### 3.1 Overall Missing-Value Analysis

### `missing_value_analysis.py`

For every column, the script calculates:

-   Missing-value count
-   Missing-value percentage

The complete feature-level missingness table is saved as:

`missing_value_report.csv`

A compact JSON summary additionally records:

  -----------------------------------------------------------------------
  Measure                             Description
  ----------------------------------- -----------------------------------
  Total missing cells                 Total number of missing entries
                                      across the dataframe

  Features with missing values        Number of columns containing at
                                      least one missing value
  -----------------------------------------------------------------------

### Generated files

-   `missing_value_report.csv`
-   `missing_value_report.json`

------------------------------------------------------------------------

### 3.2 Feature-Level Missingness Breakdown

### `missing_feature_breakdown.py`

This script provides a focused breakdown of only those features
containing missing values.

For every affected feature, it reports:

  Field                  Description
  ---------------------- ------------------------------------
  `feature`              Feature name
  `missing_count`        Number of missing observations
  `missing_percentage`   Percentage of observations missing

The results are sorted by missing count in descending order, allowing
the most affected variables to be identified immediately.

### Generated files

-   `Table_4_Missing_Feature_Breakdown.csv`
-   `missing_feature_breakdown.json`

> **Important:** This stage reports and characterizes missingness. The
> missing-value treatment itself belongs to the preprocessing pipeline
> described in Stage 1.

------------------------------------------------------------------------

## 🔗 4. Pearson Correlation Analysis

### `correlation_analysis.py`

Pearson correlation analysis is performed across the numerical variables
in the cleaned dataset.

The correlation coefficient is calculated pairwise using the numerical
feature matrix:

`numeric_df.corr()`

The resulting correlation matrix provides the pairwise linear
association between numerical variables.

### Outputs

  ------------------------------------------------------------------------
  Output                               Purpose
  ------------------------------------ -----------------------------------
  `Table_3_Correlation_Matrix.csv`     Complete numerical correlation
                                       matrix

  `correlation_matrix.json`            Machine-readable correlation matrix

  `Figure_1_Correlation_Heatmap.png`   Visual representation of pairwise
                                       correlations
  ------------------------------------------------------------------------

The heatmap is generated at high resolution (`300 dpi`) for use in
reproducibility and inspection.

------------------------------------------------------------------------

## 📊 5. EDA Outputs at a Glance

After running all Stage 2 scripts, the expected result structure is:

    results/
    └── stage2_eda/
        ├── descriptive_statistics.json
        ├── Table_1_Dataset_Characteristics.csv
        ├── Table_2_Feature_Statistics.csv
        ├── Table_3_Correlation_Matrix.csv
        ├── correlation_matrix.json
        ├── Figure_1_Correlation_Heatmap.png
        ├── missing_value_report.csv
        ├── missing_value_report.json
        ├── Table_4_Missing_Feature_Breakdown.csv
        └── missing_feature_breakdown.json

------------------------------------------------------------------------

## ▶️ 6. Reproduction

Run the Stage 2 scripts from the repository root:

    python stage2_eda/descriptive_statistics.py
    python stage2_eda/missing_value_analysis.py
    python stage2_eda/missing_feature_breakdown.py
    python stage2_eda/correlation_analysis.py

The complete analytical flow is:

    clean_master_dataframe.csv
                │
                ▼
       ┌──────────────────┐
       │ Dataset           │
       │ Characteristics   │
       └────────┬─────────┘
                │
                ├──────────────► Descriptive Statistics
                │
                ├──────────────► Missing-Value Analysis
                │
                ├──────────────► Feature Missingness
                │
                └──────────────► Pearson Correlation
                                  │
                                  ▼
                         Correlation Heatmap
                                  │
                                  ▼
                         Stage 2 EDA Outputs

------------------------------------------------------------------------

## 📄 7. Relationship to the Submitted Manuscript

The submitted manuscript describes EDA as part of the multimodal dataset
analysis and explicitly uses the **Pearson correlation coefficient** to
examine relationships among the numerical variables.

The manuscript defines the Pearson correlation coefficient as:

    r =
        Σ(xᵢ − x̄)(yᵢ − ȳ)
        ─────────────────────────────
        √[Σ(xᵢ − x̄)²] √[Σ(yᵢ − ȳ)²]

The EDA stage therefore provides the statistical characterization and
correlation analysis preceding RHRS construction and temporal
forecasting.

------------------------------------------------------------------------

## 📊 8. Dataset Characteristics Reported in the Study

The submitted manuscript reports the following dataset configuration:

  Property                          Reported value
  ------------------------------- ----------------
  👥 Participants                               42
  📥 Data sources                                6
  🧩 Feature categories                          6
  📊 Forecast features                          23
  🧬 RHRS dimensions                             5
  🗓️ Temporal window                       14 days
  🔮 Forecast horizons               7 and 14 days
  📈 7-day forecasting samples               4,819
  📈 14-day forecasting samples              4,525

These values are reported in the manuscript's dataset summary table and
are provided here to connect the repository outputs with the submitted
experimental setup.

------------------------------------------------------------------------

## 🖼️ 9. Correlation Visualization

The generated:

`Figure_1_Correlation_Heatmap.png`

provides a visual representation of the pairwise Pearson correlations
among the numerical variables.

The submitted manuscript also presents a correlation heatmap as part of
**Figure 3(b)** in the visual analysis of the WomenHealthAI framework.

The repository version provides the underlying correlation matrix in
both CSV and JSON formats so that the visualization can be independently
regenerated or inspected numerically.

------------------------------------------------------------------------

## 🔄 10. Position in the WomenHealthAI Pipeline

    🔗 Stage 1
    Data Integration & Preprocessing
              │
              ▼
    📊 Stage 2
    Exploratory Data Analysis
              │
              ├── Dataset Characteristics
              ├── Descriptive Statistics
              ├── Missing-Value Analysis
              └── Pearson Correlation
              │
              ▼
    🧬 Stage 3
    RHRS Construction
              │
              ▼
    ✅ Stage 4
    RHRS Validation
              │
              ▼
    📈 Stage 5
    Temporal Forecasting
              │
              ▼
    🧪 Stage 5
    Ablation Analysis
              │
              ▼
    🔍 Stage 6
    Explainability
              │
              ▼
    🎯 Stage 7
    Personalized Intervention
              │
              ▼
    🤖 Stage 8
    LLM-Based Guidance

------------------------------------------------------------------------

## 🔐 11. Data Access & Reproducibility

The scripts in this stage operate on the processed participant-level
dataset generated from the authorized study data.

The original participant-level mcPHASES records are **not redistributed
in this repository**.

Researchers reproducing the analysis should obtain the dataset through
the applicable authorized data-access procedure and place the permitted
local copy in the expected project structure:

    data/
    └── processed/
        └── clean_master_dataframe.csv

The scripts then reproduce the Stage 2 descriptive, missingness, and
correlation analyses locally.

No participant-specific records or individual health reports are
required to be committed to the public repository.

------------------------------------------------------------------------

## 🧪 12. Reproducibility Principle

Stage 2 is intentionally separated from the downstream modeling stages.

Its role is to provide a transparent statistical description of the
processed dataset before:

-   RHRS formulation,
-   RHRS validation,
-   temporal sequence construction,
-   forecasting,
-   explainability,
-   intervention generation, and
-   LLM-based guidance.

This separation allows the exploratory statistics and correlation
structure to be independently inspected without coupling the EDA
implementation to the forecasting models.

------------------------------------------------------------------------

> **Repository note:** The numerical results generated by these scripts
> should be interpreted together with the corresponding tables and
> figures in the submitted manuscript. Fictional examples, if provided
> elsewhere in the repository, are clearly labelled as illustrative and
> are not substitutes for the reported study results.
