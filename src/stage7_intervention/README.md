# 🩺 Stage 7 --- Personalized Intervention Recommendation

> **Purpose:** Convert participant-level reproductive health resilience
> measurements into resilience-risk categories and personalized
> intervention recommendations.

Stage 7 forms the **personalized intervention layer** of the
WomenHealthAI framework.

It receives the processed RHRS dataset produced by the earlier stages
and performs two main operations:

1.  **Resilience risk stratification**
2.  **Personalized intervention recommendation**

The resulting recommendations are written to a structured CSV file that
can subsequently be used by the LLM-based health-guidance stage. The
recommendations are generated from the participant's latest observed
RHRS profile; they are not direct clinical treatment decisions.

------------------------------------------------------------------------

# 📌 Stage Overview

The Stage 7 workflow is:

**RHRS Dataset → Latest Participant Record → Risk Classification →
Dimension-Level Intervention Rules → Personalized Recommendations**

The implementation consists of five Python modules:

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `risk_stratification.py`            Classifies participants into
                                      resilience categories

  `resilience_interventions.py`       Generates interventions from the
                                      five RHRS dimensions

  `intervention_engine.py`            Main Stage 7 execution pipeline

  `intervention_evaluation.py`        Summarizes the resulting risk
                                      distribution

  `intervention_rules.py`             Additional feature-level
                                      intervention rules
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 📂 Directory Structure

    stage7_intervention/
    │
    ├── intervention_engine.py
    ├── resilience_interventions.py
    ├── intervention_evaluation.py
    ├── intervention_rules.py
    ├── risk_stratification.py
    │
    └── README.md

The Stage 7 results are written to:

    results/
    └── stage7_intervention/
        └── intervention_recommendations.csv

------------------------------------------------------------------------

# 1️⃣ Input Dataset

Stage 7 uses the processed RHRS dataset:

    data/processed/rhrs_dataset.csv

The dataset is loaded using:

    pd.read_csv(
        "data/processed/rhrs_dataset.csv"
    )

The intervention engine sorts the observations using:

    id
    day_in_study

and selects the **latest available record for each participant**.

Therefore, intervention recommendations are generated from the
participant's most recent available RHRS profile rather than from every
longitudinal observation.

------------------------------------------------------------------------

# 2️⃣ Participant-Level Processing

For each participant, the intervention engine performs:

    Participant Records
           │
           ▼
    Sort by day_in_study
           │
           ▼
    Select latest record
           │
           ▼
    RHRS Risk Classification
           │
           ▼
    Dimension-Level Intervention Rules
           │
           ▼
    Personalized Recommendation
           │
           ▼
    Output CSV

The latest record is obtained using participant grouping followed by:

    groupby("id").tail(1)

This ensures that one intervention profile is generated per participant.

------------------------------------------------------------------------

# 3️⃣ Risk Stratification

### Script

    risk_stratification.py

The function:

    classify_risk(rhrs)

maps the overall RHRS value to one of four resilience categories.

The thresholds implemented in the code are:

         RHRS Range Risk/Resilience Category
  ----------------- --------------------------
          RHRS ≥ 70 High Resilience
    50 ≤ RHRS \< 70 Moderate Resilience
    30 ≤ RHRS \< 50 Low Resilience
         RHRS \< 30 Critical

The implementation directly applies these thresholds.
:chatgpt-content-reference{index="3"}

------------------------------------------------------------------------

# 4️⃣ Relationship to the Manuscript

The manuscript defines the resilience categories using:

    High:
        RHRS ≥ 70

    Moderate:
        50 ≤ RHRS < 70

    Low:
        30 ≤ RHRS < 50

    Critical:
        RHRS < 30

These categories are presented as Equation (19) in the manuscript.
:chatgpt-content-reference{index="4"}

Therefore, the Stage 7 implementation is directly consistent with the
manuscript's RHRS stratification scheme.

------------------------------------------------------------------------

# 5️⃣ Resilience Dimensions

The personalized intervention engine evaluates the five RHRS dimensions:

    HRS
    PRS
    MRS
    BRS
    SRS

These represent:

  Dimension   Meaning
  ----------- --------------------------------
  HRS         Hormonal Resilience Score
  PRS         Physiological Resilience Score
  MRS         Metabolic Resilience Score
  BRS         Behavioral Resilience Score
  SRS         Symptom Resilience Score

The manuscript defines these as the five complementary dimensions of
RHRS. :chatgpt-content-reference{index="5"}

------------------------------------------------------------------------

# 6️⃣ Dimension-Level Intervention Rules

### Script

    resilience_interventions.py

The function:

    generate_resilience_interventions(patient)

generates recommendations according to the participant's individual
resilience dimensions.

The current implementation uses:

    Score < 50

as the intervention trigger for each resilience dimension.

------------------------------------------------------------------------

# 7️⃣ Hormonal Resilience Intervention

The HRS rule is:

    if HRS < 50

The system generates:

    Hormonal resilience is reduced.
    Monitor hormonal fluctuations and consider endocrine evaluation.

This recommendation is generated only when the participant's HRS falls
below 50. :chatgpt-content-reference{index="6"}

------------------------------------------------------------------------

# 8️⃣ Psychological / Physiological Resilience Intervention

The current implementation uses the variable:

    PRS

When:

    PRS < 50

the system generates:

    Psychological resilience is low.
    Stress management and mental wellness support are recommended.

This is the exact intervention rule implemented in the current Stage 7
code. :chatgpt-content-reference{index="7"}

------------------------------------------------------------------------

# 9️⃣ Metabolic Resilience Intervention

When:

    MRS < 50

the system generates:

    Metabolic resilience is reduced.
    Improve nutrition, glucose regulation, and physical activity.

This connects the metabolic resilience deficit to nutrition, glucose
regulation, and physical activity recommendations.
:chatgpt-content-reference{index="8"}

------------------------------------------------------------------------

# 🔟 Behavioral Resilience Intervention

When:

    BRS < 50

the system generates:

    Behavioral resilience is low.
    Improve sleep hygiene and daily health routines.

The intervention therefore targets behavioral and routine-related
factors when BRS falls below the intervention threshold.
:chatgpt-content-reference{index="9"}

------------------------------------------------------------------------

# 1️⃣1️⃣ Symptom Resilience Intervention

When:

    SRS < 50

the system generates:

    Symptom resilience is reduced.
    Increased symptom monitoring is recommended.

This provides a symptom-monitoring recommendation for participants with
reduced SRS. :chatgpt-content-reference{index="10"}

------------------------------------------------------------------------

# 1️⃣2️⃣ Overall RHRS Intervention

In addition to the five individual resilience dimensions, the
intervention engine checks:

    RHRS < 40

When this condition is satisfied, it generates:

    Overall resilience is low.
    Comprehensive intervention and closer monitoring are recommended.

This rule is implemented separately from the four-category RHRS risk
classification. :chatgpt-content-reference{index="11"}

------------------------------------------------------------------------

# 1️⃣3️⃣ Stable Profile

If none of the intervention conditions are triggered, the system
generates:

    Current resilience profile is stable.
    Maintain present lifestyle and monitoring practices.

This prevents participants from receiving an empty recommendation field.
:chatgpt-content-reference{index="12"}

------------------------------------------------------------------------

# 1️⃣4️⃣ Intervention Generation Logic

The current intervention engine therefore follows:

    HRS < 50
       │
       └──► Hormonal intervention

    PRS < 50
       │
       └──► Psychological / mental-wellness intervention

    MRS < 50
       │
       └──► Metabolic intervention

    BRS < 50
       │
       └──► Behavioral / sleep intervention

    SRS < 50
       │
       └──► Symptom-monitoring intervention

    RHRS < 40
       │
       └──► Comprehensive intervention

If none are triggered:

    Stable-profile recommendation

Multiple rules can be triggered for the same participant.

Therefore, a participant can receive several personalized
recommendations simultaneously.

------------------------------------------------------------------------

# 1️⃣5️⃣ Main Intervention Engine

### Script

    intervention_engine.py

This is the main Stage 7 execution script.

It performs the complete pipeline:

    1. Load RHRS dataset
    2. Sort participant observations
    3. Select latest participant record
    4. Calculate resilience category
    5. Generate personalized interventions
    6. Combine recommendations
    7. Save results

The engine imports:

    classify_risk

from:

    risk_stratification.py

and:

    generate_resilience_interventions

from:

    resilience_interventions.py

This dependency structure is explicitly present in the implementation.
:chatgpt-content-reference{index="13"}

------------------------------------------------------------------------

# 1️⃣6️⃣ Participant-Level Output

For every participant, the engine creates:

    Participant
    RHRS
    Risk
    Interventions

The implementation constructs these fields before adding the record to
the output dataframe. :chatgpt-content-reference{index="14"}

The resulting structure is:

  Column            Description
  ----------------- -------------------------------------------
  `Participant`     Participant identifier
  `RHRS`            Latest RHRS value
  `Risk`            Resilience category
  `Interventions`   Personalized intervention recommendations

------------------------------------------------------------------------

# 1️⃣7️⃣ Output File

The final recommendations are written to:

    results/stage7_intervention/
    └── intervention_recommendations.csv

The output is generated using:

    results.to_csv(
        RESULTS_DIR /
        "intervention_recommendations.csv",
        index=False
    )

The results directory is automatically created if it does not already
exist.

The CSV is an analysis artifact containing participant-level
information. It should only be retained or shared within an authorized
analysis environment; public repository releases should exclude
participant identifiers and individual-level recommendation records
unless their release is explicitly authorized.
:chatgpt-content-reference{index="15"}
:chatgpt-content-reference{index="16"}

------------------------------------------------------------------------

# 1️⃣8️⃣ Example Output Structure

The resulting CSV follows the structure:

    Participant,RHRS,Risk,Interventions

For example:

    P001,58.29,Moderate Resilience,
    "Behavioral resilience is low. Improve sleep hygiene and daily health routines.;
     Symptom resilience is reduced. Increased symptom monitoring is recommended."

The exact recommendations depend on the participant's latest observed
HRS, PRS, MRS, BRS, SRS, and RHRS values. These observed values are used
to describe the participant's current profile rather than treating a
forecasted RHRS value as an already observed clinical state.

------------------------------------------------------------------------

# 1️⃣9️⃣ Intervention Evaluation

### Script

    intervention_evaluation.py

This module reads:

    results/stage7_intervention/intervention_recommendations.csv

and evaluates the distribution of the generated resilience categories.

The current implementation calculates:

    results["Risk"].value_counts()

and prints the resulting risk distribution.
:chatgpt-content-reference{index="17"}

------------------------------------------------------------------------

# 2️⃣0️⃣ Risk Distribution Analysis

The evaluation stage therefore provides the number of participants in
each category:

    High Resilience
    Moderate Resilience
    Low Resilience
    Critical

This provides a simple participant-level summary of the resilience-risk
stratification generated by Stage 7.

------------------------------------------------------------------------

# 2️⃣1️⃣ Additional Intervention Rules

### Script

    intervention_rules.py

This file contains an additional rule-based intervention generator:

    generate_interventions(patient)

Unlike `resilience_interventions.py`, these rules operate directly on
individual physiological and behavioral measurements.

The current rules include:

  Variable         Condition   Recommendation Focus
  ---------------- ----------- --------------------------------
  `sleep_score`    \< 60       Sleep hygiene
  `stress_score`   \> 70       Stress reduction
  `mean_rmssd`     \< 40       Recovery / physical strain
  `resting_hr`     \> 75       Cardiovascular monitoring
  `mean_glucose`   \> 110      Dietary and glucose management

The implementation of these rules is contained in
`intervention_rules.py`. :chatgpt-content-reference{index="18"}

------------------------------------------------------------------------

# 2️⃣2️⃣ Important Implementation Distinction

The repository currently contains **two intervention-rule approaches**.

### Approach A --- Used by the main engine

    resilience_interventions.py

This operates on:

    HRS
    PRS
    MRS
    BRS
    SRS
    RHRS

and is directly imported by:

    intervention_engine.py

### Approach B --- Separate feature-level rule module

    intervention_rules.py

This operates on:

    sleep_score
    stress_score
    mean_rmssd
    resting_hr
    mean_glucose

However, `intervention_engine.py` does not currently import
`generate_interventions()` from `intervention_rules.py`.

Therefore, **Approach A is the active Stage 7 intervention pipeline in
the current implementation**.

------------------------------------------------------------------------

# 2️⃣3️⃣ Relationship to the RHRS Framework

The RHRS itself is calculated from five resilience dimensions:

    HRS
    PRS
    MRS
    BRS
    SRS

The manuscript defines the final RHRS as:

    RHRS =
        0.25 HRS
      + 0.25 PRS
      + 0.15 MRS
      + 0.20 BRS
      + 0.15 SRS

with RHRS ranging from 0 to 100. :chatgpt-content-reference{index="19"}

Stage 7 uses this resulting resilience profile for downstream
intervention generation.

------------------------------------------------------------------------

# 2️⃣4️⃣ Manuscript Intervention Methodology

The manuscript describes personalized intervention as a two-step
process:

    RHRS Prediction
          │
          ▼
    Resilience Category
          │
          ▼
    Intervention Prioritization
          │
          ▼
    Personalized Recommendations

The manuscript defines an intervention priority score:

    Pi = 100 − Ri

where:

    Ri ∈ {HRS, PRS, MRS, BRS, SRS}

and states that higher priority values correspond to resilience
dimensions requiring greater attention.
:chatgpt-content-reference{index="20"}

------------------------------------------------------------------------

# 2️⃣5️⃣ Current Code vs. Manuscript Priority Score

An important reproducibility note:

The current Stage 7 code does **not explicitly calculate**:

    Pi = 100 − Ri

and does not sort the five dimensions by that priority score.

Instead, the current implementation:

    1. Classifies overall RHRS
    2. Checks each resilience dimension against a threshold
    3. Appends the corresponding intervention text
    4. Combines all triggered interventions

Therefore, the repository currently implements **threshold-based
personalized intervention generation**, while the manuscript describes
the broader intervention methodology in terms of priority scores and
ranking.

This distinction should be preserved unless the implementation is
subsequently updated.

------------------------------------------------------------------------

# 2️⃣6️⃣ Connection to Stage 6

Stage 7 follows the explainability stage.

The overall pipeline is:

    Stage 5
    Temporal Forecasting
          │
          ▼
    Stage 6
    Explainability
          │
          ▼
    Stage 7
    Personalized Intervention
          │
          ▼
    Stage 8
    LLM-Based Health Guidance

The manuscript describes this sequential decision-support pipeline as
transforming observations into RHRS, forecasting future resilience,
explaining influential factors, converting identified deficiencies into
intervention targets, and then communicating the resulting information
through LLM-based guidance. :chatgpt-content-reference{index="21"}

------------------------------------------------------------------------

# 2️⃣7️⃣ Connection to LLM-Based Guidance

Stage 7 produces structured intervention recommendations that can
subsequently be consumed by the LLM-based guidance module.

The manuscript states that Llama-3 is used to generate personalized
reproductive-health reports from the predicted resilience profile and
corresponding intervention recommendations. Stage 7 itself remains a
rule-based recommendation layer and does not perform LLM-based
generation. :chatgpt-content-reference{index="22"}

Therefore:

    Stage 7
       │
       ├── RHRS
       ├── Risk Category
       └── Intervention Recommendations
                │
                ▼
           LLM Guidance
                │
                ▼
        Patient-Friendly Report

------------------------------------------------------------------------

# 2️⃣8️⃣ Manuscript Example

The manuscript provides an example of a participant with:

    RHRS = 58.29

who was classified as:

    Moderate Resilience

The corresponding intervention profile included recommendations related
to:

    • Sleep quality
    • Daily health routines
    • Symptom monitoring

These recommendations were subsequently translated into a
patient-friendly report using Llama-3.
:chatgpt-content-reference{index="23"}

------------------------------------------------------------------------

# 2️⃣9️⃣ Reproducibility Procedure

## Step 1 --- Ensure the RHRS Dataset Exists

Required file:

    data/processed/rhrs_dataset.csv

The dataset must contain at least the variables required by the
intervention engine:

    id
    day_in_study
    RHRS
    HRS
    PRS
    MRS
    BRS
    SRS

------------------------------------------------------------------------

## Step 2 --- Run the Intervention Engine

From the project root:

    python intervention_engine.py

The engine:

    • Loads the processed dataset
    • Selects the latest participant record
    • Classifies resilience
    • Generates interventions
    • Saves the recommendations

------------------------------------------------------------------------

## Step 3 --- Verify the Output

Expected output:

    results/stage7_intervention/
    └── intervention_recommendations.csv

------------------------------------------------------------------------

## Step 4 --- Evaluate Risk Distribution

Run:

    python intervention_evaluation.py

This prints the participant distribution across the four resilience
categories.

------------------------------------------------------------------------

# 3️⃣0️⃣ Complete Stage 7 Workflow

    data/processed/rhrs_dataset.csv
                 │
                 ▼
       Latest Participant Record
                 │
                 ▼
          ┌──────────────┐
          │ RHRS Value   │
          └──────┬───────┘
                 │
                 ▼
        Risk Stratification
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
      High   Moderate    Low
                 │
                 ▼
              Critical
                 │
                 ▼
      Five-Dimension Analysis
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
      HRS       PRS       MRS
       │         │         │
       └────┬────┴────┬────┘
            ▼         ▼
           BRS       SRS
            │         │
            └────┬────┘
                 ▼
       Personalized Intervention
                 │
                 ▼
    intervention_recommendations.csv
                 │
                 ▼
        Stage 8 LLM Guidance

------------------------------------------------------------------------

# 3️⃣1️⃣ Output-to-Script Mapping

  --------------------------------------------------------------------------------------------
  Script                          Function                Output
  ------------------------------- ----------------------- ------------------------------------
  `risk_stratification.py`        RHRS category           Risk category
                                  classification          

  `resilience_interventions.py`   Dimension-based         Intervention list
                                  recommendations         

  `intervention_engine.py`        Complete Stage 7        `intervention_recommendations.csv`
                                  pipeline                

  `intervention_evaluation.py`    Risk distribution       Console summary
                                  analysis                

  `intervention_rules.py`         Additional              Recommendation list when called
                                  feature-level rules     independently
  --------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 3️⃣2️⃣ Stage 7 Input--Output Summary

  -----------------------------------------------------------------------
  Component               Input                   Output
  ----------------------- ----------------------- -----------------------
  Risk Stratification     RHRS                    Risk category

  Resilience Intervention HRS, PRS, MRS, BRS,     Intervention
  Engine                  SRS, RHRS               recommendations

  Main Engine             Participant-level       CSV
                          latest records          

  Evaluation              Intervention CSV        Risk distribution

  Additional Rule Engine  Sleep, stress, HRV,     Feature-level
                          RHR, glucose            recommendations
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 3️⃣3️⃣ Safety and Interpretation Scope

The intervention engine is a **research prototype for personalized
decision support**.

Its recommendations are generated from predefined numerical thresholds
and rule-based mappings.

They should therefore be interpreted as computational recommendations
rather than clinical diagnoses or individualized medical treatment
decisions. The thresholds are research-prototype rules and should not be
interpreted as validated clinical cutoffs.

The manuscript itself identifies uncertainty propagation as an important
limitation because intervention priorities may be derived from predicted
rather than directly observed RHRS values. It identifies
uncertainty-aware intervention strategies as an area for future work.
:chatgpt-content-reference{index="24"}

------------------------------------------------------------------------

# 3️⃣4️⃣ Stage 7 Summary

Stage 7 converts the participant's latest reproductive-health resilience
profile into actionable intervention recommendations.

The implemented pipeline provides:

    ✔ Latest participant-level RHRS profile
    ✔ Four-category resilience stratification
    ✔ HRS-based intervention
    ✔ PRS-based intervention
    ✔ MRS-based intervention
    ✔ BRS-based intervention
    ✔ SRS-based intervention
    ✔ Overall RHRS intervention
    ✔ Stable-profile recommendation
    ✔ Participant-level CSV output
    ✔ Risk-distribution evaluation
    ✔ Integration with downstream LLM guidance

The current implementation is therefore a **threshold-based, rule-driven
personalized intervention engine** operating on the RHRS framework.

It provides the bridge between:

    Explainable RHRS Forecasting

and:

    LLM-Based Personalized Health Guidance
