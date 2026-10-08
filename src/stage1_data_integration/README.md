# 🔗 Stage 1 --- Data Integration & Preprocessing

> **Purpose:** Construct the unified participant-day multimodal dataset
> used as the foundation of the WomenHealthAI framework.

This stage integrates heterogeneous reproductive-health measurements
into a common participant-day representation and performs the initial
cleaning and encoding required by the downstream RHRS, forecasting,
validation, explainability, intervention, and LLM-guidance stages.

------------------------------------------------------------------------

## 📌 Stage Overview

  ------------------------------------------------------------------------------
  Script                  Purpose                 Main Output
  ----------------------- ----------------------- ------------------------------
  `merge_data.py`         Integrates the          `master_dataframe.csv`
                          multimodal source       
                          datasets at the         
                          participant-day level   

  `clean_data.py`         Removes duplicates,     `clean_master_dataframe.csv`
                          encodes symptoms, and   
                          handles numerical       
                          missing values          
  ------------------------------------------------------------------------------

The processing pipeline is:

**Raw multimodal data → Daily aggregation → Participant-day integration
→ Cleaning → Processed dataset**

------------------------------------------------------------------------

## 📥 1. Multimodal Data Integration

### `merge_data.py`

The integration script loads the six source datasets used by the
framework:

  -----------------------------------------------------------------------------------------
                            \# Source Dataset                         Modality
  ---------------------------- -------------------------------------- ---------------------
                             1 `hormones_and_selfreport.csv`          Hormonal &
                                                                      self-reported
                                                                      measurements

                             2 `heart_rate_variability_details.csv`   Heart-rate
                                                                      variability

                             3 `resting_heart_rate.csv`               Resting heart rate

                             4 `sleep_score.csv`                      Sleep

                             5 `stress_score.csv`                     Stress

                             6 `glucose.csv`                          Metabolic / glucose
                                                                      measurements
  -----------------------------------------------------------------------------------------

All modalities are aligned using:

-   👤 **Participant identifier:** `id`
-   📅 **Study time index:** `day_in_study`

High-frequency measurements are aggregated to the **participant-day
level** before being merged into the unified multimodal dataset.

------------------------------------------------------------------------

## 📊 2. Daily Feature Construction

The following daily features are generated during integration:

  -----------------------------------------------------------------------
  Modality                            Daily features
  ----------------------------------- -----------------------------------
  ❤️ HRV                              Mean RMSSD, RMSSD standard
                                      deviation, mean LF, mean HF, HRV
                                      sample count

  🩸 Glucose                          Mean glucose, glucose standard
                                      deviation, minimum glucose, maximum
                                      glucose

  💓 Resting Heart Rate               Mean resting heart rate

  😴 Sleep                            Sleep score, composition score,
                                      revitalization score, duration
                                      score, deep sleep, restlessness

  🧠 Stress                           Mean stress score

  🧬 Hormonal / Self-report           Retained from the corresponding
                                      source dataset
  -----------------------------------------------------------------------

The resulting modality-specific tables are merged using `id` and
`day_in_study` to create the unified participant-day dataframe.

------------------------------------------------------------------------

## 🧹 3. Initial Data Cleaning

### `clean_data.py`

The cleaning stage operates on:

`data/processed/master_dataframe.csv`

It performs three primary operations.

### 3.1 🗑️ Duplicate Removal

Completely duplicated observations are identified and removed before
subsequent processing.

### 3.2 🔢 Symptom Encoding

Ordinal symptom responses are converted into numerical values:

  Response       Encoded value
  ------------ ---------------
  Not at all               `0`
  Very Low                 `1`
  Low                      `2`
  Moderate                 `3`
  High                     `4`
  Very High                `5`

The encoded symptom variables include, where available:

-   Headaches
-   Cramps
-   Sore breasts
-   Fatigue
-   Sleep issues
-   Mood swings
-   Stress
-   Food cravings
-   Indigestion
-   Bloating

### 3.3 🩹 Missing-Value Handling

Missing values in numerical columns are replaced using the **median of
the corresponding numerical column** in the dataframe processed by this
stage. **This operation is part of the cohort-level construction and
harmonization of the unified multimodal participant-day dataset and
establishes the common analytical representation used by subsequent
stages.**

The implementation records the number of missing values before and after
this operation.

### 3.4 🔒 Training-Only Preprocessing for Forecasting

For the downstream temporal forecasting experiments, any data-dependent
preprocessing parameters used for model inputs are estimated from the
training partition only.

The chronological training partition is established before fitting such
parameters. The fitted parameters are then applied unchanged to the
validation and test partitions.

This prevents information from the validation or test periods from
contributing to preprocessing decisions and avoids temporal information
leakage.

The Stage 1 integrated and cleaned dataset is therefore treated as the
input dataset for downstream chronological partitioning, while
training-dependent preprocessing is applied within the forecasting
workflow after the temporal split has been established.

------------------------------------------------------------------------

## 📦 4. Generated Outputs

After successful execution, the following data products are generated:

    data/
    └── processed/
        ├── master_dataframe.csv
        └── clean_master_dataframe.csv

    results/
    └── stage1_data_integration/
        ├── integration_report.json
        ├── participant_summary.json
        ├── feature_summary.json
        └── cleaning_report.json

### 📋 Output Reports

  -----------------------------------------------------------------------
  Report                              Contents
  ----------------------------------- -----------------------------------
  `integration_report.json`           Participant count, number of rows,
                                      number of columns, and generated
                                      features

  `participant_summary.json`          Number of observations available
                                      for each participant

  `feature_summary.json`              Mean, standard deviation, minimum,
                                      and maximum of numerical features

  `cleaning_report.json`              Rows before/after cleaning,
                                      duplicates removed, and
                                      missing-value statistics
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## ▶️ 5. Reproduction

From the repository root, execute:

    python stage1_data_integration/merge_data.py
    python stage1_data_integration/clean_data.py

The complete Stage 1 workflow is:

    RAW MULTIMODAL DATA
             │
             ▼
    ┌──────────────────────┐
    │  Multimodal Sources  │
    │                      │
    │ Hormones / Self-report
    │ HRV / RHR            │
    │ Sleep / Stress       │
    │ Glucose              │
    └──────────┬───────────┘
               │
               ▼
    Daily Participant-Level
         Aggregation
               │
               ▼
    Participant-Day Alignment
               │
               ▼
      master_dataframe.csv
               │
               ▼
    ┌──────────────────────┐
    │    Initial Cleaning  │
    │                      │
    │ • Duplicate removal  │
    │ • Symptom encoding   │
    │ • Missing values     │
    └──────────┬───────────┘
               │
               ▼
    clean_master_dataframe.csv

------------------------------------------------------------------------

## 📄 6. Connection to the Submitted Manuscript

This stage corresponds primarily to **Section II-A --- Multimodal
Dataset Construction and Analysis** of the submitted WomenHealthAI
manuscript.

The manuscript describes the construction of a unified participant-day
multimodal dataset from the mcPHASES repository by integrating hormonal,
physiological, metabolic, behavioral, sleep, stress, glucose, and
symptom-related measurements.

The resulting processed dataset is subsequently used by the downstream
WomenHealthAI stages for:

-   🧬 RHRS construction
-   📈 Temporal forecasting
-   ✅ RHRS validation
-   🔍 Explainability analysis
-   🎯 Personalized intervention
-   🤖 LLM-based health guidance

------------------------------------------------------------------------

## 🔄 Stage Position in the Framework

    🔗 Stage 1
    Data Integration & Preprocessing
              │
              ▼
    📊 Stage 2
    Exploratory Data Analysis
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

> **Note:** The original participant-level mcPHASES data are not
> redistributed through this repository. The repository provides the
> computational implementation used to construct and process the study
> data while respecting the applicable data-access restrictions.
