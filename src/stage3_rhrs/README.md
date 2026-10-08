# 🧬 Stage 3 --- Reproductive Health Resilience Score (RHRS)

> **Purpose:** Construct the five-dimensional Reproductive Health
> Resilience Score (RHRS) from the cleaned multimodal participant-day
> dataset and generate the component-level and overall resilience scores
> used by the downstream validation and forecasting stages.

Stage 3 implements the RHRS formulation described in the submitted
WomenHealthAI manuscript.

The framework represents reproductive health through five complementary
dimensions:

  -----------------------------------------------------------------------
  Dimension               Abbreviation            Main measurements
  ----------------------- ----------------------- -----------------------
  🧬 Hormonal Resilience  `HRS`                   LH, estrogen, PdG
  Score                                           

  ❤️ Physiological        `PRS`                   RMSSD, LF, HF, resting
  Resilience Score                                heart rate

  🩸 Metabolic Resilience `MRS`                   Mean glucose, glucose
  Score                                           variability

  😴 Behavioral           `BRS`                   Sleep score, deep
  Resilience Score                                sleep, stress

  🩹 Symptom Resilience   `SRS`                   Headache, cramps,
  Score                                           fatigue, food cravings,
                                                  bloating, stress

  🌸 Overall Reproductive `RHRS`                  Weighted combination of
  Health Resilience Score                         HRS, PRS, MRS, BRS and
                                                  SRS
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 📌 1. Stage Structure

The Stage 3 implementation contains seven scripts:

  ---------------------------------------------------------------------------------
  Script                          Function                Output
  ------------------------------- ----------------------- -------------------------
  `hormonal_resilience.py`        Computes HRS            `Table_5_HRS.csv`

  `physiological_resilience.py`   Computes PRS            `Table_6_PRS.csv`

  `metabolic_resilience.py`       Computes MRS            `Table_7_MRS.csv`

  `behavioral_resilience.py`      Computes BRS            `Table_8_BRS.csv`

  `symptom_resilience.py`         Computes SRS            `Table_9_SRS.csv`

  `compute_rhrs.py`               Combines all five       `Table_10_RHRS.csv`,
                                  dimensions into RHRS    `rhrs_dataset.csv`

  `rhrs_diagnostics.py`           Produces summary        `rhrs_diagnostics.json`
                                  statistics for all RHRS 
                                  dimensions              
  ---------------------------------------------------------------------------------

All component scripts operate on:

    data/processed/clean_master_dataframe.csv

The resulting RHRS dataset is written to:

    data/processed/rhrs_dataset.csv

and Stage 3 outputs are stored in:

    results/stage3_rhrs/

------------------------------------------------------------------------

# 🧮 2. Common Normalization Strategy

The component scores use percentile normalization to place heterogeneous
measurements on a common 0--100 scale.

For a feature `x`, the implementation uses:

    PR(x) = rank(x) / N × 100

where:

-   `rank(x)` is the ascending rank of the observation,
-   `N` is the number of observations,
-   larger percentile values correspond to larger observed feature
    values.

This allows measurements with different physical units and numerical
ranges to contribute to a common resilience scale.

The manuscript defines the same percentile normalization in Eq. (3).

This percentile transformation is part of the RHRS definition and
establishes a common analytical scale across the heterogeneous
measurements; it is not a trainable parameter of the downstream
forecasting models.

------------------------------------------------------------------------

# 🧬 3. Hormonal Resilience Score --- HRS

### Script

    hormonal_resilience.py

### Input features

  Feature      Meaning
  ------------ -------------------------------
  `lh`         Luteinizing hormone
  `estrogen`   Estrogen
  `pdg`        Progesterone metabolite (PdG)

Each feature is converted to a percentile rank.

The implementation then computes:

    HRS = [PR(LH) + PR(Estrogen) + PR(PdG)] / 3

The resulting score is clipped to the interval:

    0 ≤ HRS ≤ 100

The manuscript presents the same formulation in Eq. (4).

### Output

    results/stage3_rhrs/Table_5_HRS.csv

Each row contains:

  Column           Description
  ---------------- ---------------------------
  `id`             Participant identifier
  `day_in_study`   Study day
  `HRS`            Hormonal resilience score

A summary containing the mean, standard deviation, minimum and maximum
is also written to:

    results/stage3_rhrs/hormonal_resilience.json

------------------------------------------------------------------------

# ❤️ 4. Physiological Resilience Score --- PRS

### Script

    physiological_resilience.py

### Input features

  Feature        Measurement
  -------------- -------------------------
  `mean_rmssd`   Mean RMSSD
  `mean_lf`      Mean low-frequency HRV
  `mean_hf`      Mean high-frequency HRV
  `resting_hr`   Resting heart rate

RMSSD, LF and HF are percentile normalized directly.

For resting heart rate, the implementation first computes the percentile
rank and then reverses its direction:

    RHR_score = 100 − PR(RHR)

This reflects the formulation stated in the manuscript that lower
resting heart rate is treated as contributing positively to the
physiological resilience score.

The physiological score is then:

    PRS =
    [PR(RMSSD) + PR(LF) + PR(HF) + RHR_score] / 4

The final value is clipped to:

    0 ≤ PRS ≤ 100

### Output

    results/stage3_rhrs/Table_6_PRS.csv

------------------------------------------------------------------------

# 🩸 5. Metabolic Resilience Score --- MRS

### Script

    metabolic_resilience.py

### Input features

  Feature          Measurement
  ---------------- ---------------------
  `mean_glucose`   Mean glucose
  `std_glucose`    Glucose variability

Both variables are percentile normalized.

The implementation reverses both directions:

    glucose_health = 100 − PR(mean_glucose)

    variability_health = 100 − PR(std_glucose)

The metabolic resilience score is:

    MRS =
    0.6 × glucose_health
    +
    0.4 × variability_health

Therefore:

    MRS =
    0.6 × [100 − PR(mean_glucose)]
    +
    0.4 × [100 − PR(std_glucose)]

The final score is clipped to:

    0 ≤ MRS ≤ 100

The weighting gives mean glucose a larger contribution than glucose
variability.

### Output

    results/stage3_rhrs/Table_7_MRS.csv

------------------------------------------------------------------------

# 😴 6. Behavioral Resilience Score --- BRS

### Script

    behavioral_resilience.py

### Input features

  Feature          Role
  ---------------- -------------------------
  `sleep_score`    Sleep quality component
  `deep_sleep`     Deep-sleep component
  `stress_score`   Stress penalty

Sleep score and deep sleep are percentile normalized.

Stress is also percentile normalized.

The sleep component is:

    Sleep_component =
    [PR(Sleep) + PR(DeepSleep)] / 2

The stress penalty is:

    Stress_penalty =
    0.3 × PR(Stress)

The behavioral resilience score is:

    BRS =
    Sleep_component − Stress_penalty

or equivalently:

    BRS =
    [PR(Sleep) + PR(DeepSleep)] / 2
    − 0.3 × PR(Stress)

The resulting value is clipped to:

    0 ≤ BRS ≤ 100

### Output

    results/stage3_rhrs/Table_8_BRS.csv

------------------------------------------------------------------------

# 🩹 7. Symptom Resilience Score --- SRS

### Script

    symptom_resilience.py

### Input features

The implementation uses six symptom-related variables:

  Feature
  ----------------
  `headaches`
  `cramps`
  `fatigue`
  `foodcravings`
  `bloating`
  `stress`

The symptom variables are converted to numerical values where necessary,
with any remaining missing values handled using the corresponding
feature median.

Each variable is then percentile normalized.

The implementation first calculates symptom burden:

    Symptom_burden =
    [PR(Headache)
    + PR(Cramps)
    + PR(Fatigue)
    + PR(FoodCravings)
    + PR(Bloating)
    + PR(Stress)] / 6

Because larger symptom burden represents a less favorable resilience
state, the direction is reversed:

    SRS = 100 − Symptom_burden

The final score is clipped to:

    0 ≤ SRS ≤ 100

### Output

    results/stage3_rhrs/Table_9_SRS.csv

------------------------------------------------------------------------

# 🌸 8. Overall Reproductive Health Resilience Score --- RHRS

### Script

    compute_rhrs.py

The five component scores are first loaded:

    HRS
    PRS
    MRS
    BRS
    SRS

The overall RHRS is then calculated using the weighted formulation
reported in the manuscript:

    RHRS =
    0.25 × HRS
    +
    0.25 × PRS
    +
    0.15 × MRS
    +
    0.20 × BRS
    +
    0.15 × SRS

The weights sum to:

    0.25 + 0.25 + 0.15 + 0.20 + 0.15 = 1.00

The final RHRS is clipped to:

    0 ≤ RHRS ≤ 100

Higher RHRS values therefore represent higher overall
reproductive-health resilience under the operational definition used in
this study.

------------------------------------------------------------------------

## ⚖️ 9. Rationale for the RHRS Weighting

The submitted manuscript assigns greater weight to the hormonal and
physiological dimensions:

  Dimension       Weight
  ----------- ----------
  HRS               0.25
  PRS               0.25
  MRS               0.15
  BRS               0.20
  SRS               0.15
  **Total**     **1.00**

The manuscript describes hormonal and physiological resilience as having
greater importance for reproductive-function representation, while
metabolic, behavioral and symptom dimensions provide complementary
information.

An equal-weight formulation was also considered in the experimental
analysis:

    HRS = PRS = MRS = BRS = SRS = 0.20

The equal-weight configuration is evaluated separately in the ablation
analysis.

------------------------------------------------------------------------

# 🗓️ 10. Interpretation Across Menstrual Phases

The RHRS is designed as a continuous participant-day resilience measure
rather than a phase-specific clinical reference range.

The implementation applies percentile normalization to the observed
participant-day values of each feature. It does **not** calculate a
separate percentile scale for follicular, ovulatory, luteal, or other
menstrual phases.

This distinction is important for reproducibility.

The score therefore represents the participant's relative position
within the observed study distribution for each component rather than
asserting that the same absolute biomarker value has identical
physiological meaning at every menstrual phase.

The framework combines multiple modalities to represent
reproductive-health resilience across time, while the resulting RHRS
should be interpreted as a computational resilience index rather than a
direct clinical diagnosis or phase-specific clinical reference value.

------------------------------------------------------------------------

# 🧪 11. Worked Fictional Example

The following example is **fictional and illustrative only**.

It does not represent an actual participant and is not used to generate
any reported result in the manuscript.

Assume that after percentile normalization, one hypothetical
participant-day produces:

  Component input                       Percentile / transformed value
  ----------------------------------- --------------------------------
  LH percentile                                                     70
  Estrogen percentile                                               60
  PdG percentile                                                    50
  RMSSD percentile                                                  65
  LF percentile                                                     55
  HF percentile                                                     60
  Resting-HR score                                                  70
  Mean-glucose health score                                         60
  Glucose-variability health score                                  50
  Sleep percentile                                                  70
  Deep-sleep percentile                                             60
  Stress percentile                                                 30
  Symptom burden percentile average                                 25

### HRS

    HRS = (70 + 60 + 50) / 3
        = 60.00

### PRS

    PRS = (65 + 55 + 60 + 70) / 4
        = 62.50

### MRS

    MRS = 0.6(60) + 0.4(50)
        = 56.00

### BRS

    BRS = [(70 + 60) / 2] − 0.3(30)
        = 65.00 − 9.00
        = 56.00

### SRS

If the average normalized symptom burden is 25:

    SRS = 100 − 25
        = 75.00

### Overall RHRS

    RHRS =
    0.25(60)
    + 0.25(62.5)
    + 0.15(56)
    + 0.20(56)
    + 0.15(75)

    RHRS = 61.625

Therefore:

    RHRS ≈ 61.63

This example is intended only to demonstrate how the component scores
propagate into the overall RHRS.

------------------------------------------------------------------------

# 🔍 12. Direction of the Individual Scores

The direction of each component is important because the input variables
do not all have the same interpretation.

  -----------------------------------------------------------------------
  Component                           Higher score means
  ----------------------------------- -----------------------------------
  HRS                                 Higher percentile values of the
                                      implemented hormonal features

  PRS                                 Higher normalized HRV values and
                                      lower normalized resting HR

  MRS                                 Lower normalized mean glucose and
                                      glucose variability

  BRS                                 Better normalized sleep/deep sleep
                                      with a penalty for normalized
                                      stress

  SRS                                 Lower normalized symptom burden

  RHRS                                Higher weighted overall resilience
  -----------------------------------------------------------------------

The implementation explicitly reverses resting heart rate, glucose
measures, and symptom burden where a larger raw value is treated as less
favorable within the operational scoring formulation.

------------------------------------------------------------------------

# 📦 13. Generated Outputs

After running Stage 3, the following files are generated:

    results/
    └── stage3_rhrs/
        ├── Table_5_HRS.csv
        ├── hormonal_resilience.json
        │
        ├── Table_6_PRS.csv
        ├── physiological_resilience.json
        │
        ├── Table_7_MRS.csv
        ├── metabolic_resilience.json
        │
        ├── Table_8_BRS.csv
        ├── behavioral_resilience.json
        │
        ├── Table_9_SRS.csv
        ├── symptom_resilience.json
        │
        ├── Table_10_RHRS.csv
        ├── rhrs_summary.json
        └── rhrs_diagnostics.json

The consolidated dataset is additionally written to:

    data/processed/rhrs_dataset.csv

------------------------------------------------------------------------

# 📊 14. RHRS Diagnostic Statistics

### `rhrs_diagnostics.py`

The diagnostic script reads:

    data/processed/rhrs_dataset.csv

and calculates, for:

    HRS
    PRS
    MRS
    BRS
    SRS
    RHRS

the following descriptive statistics:

  Statistic
  --------------------
  Mean
  Standard deviation
  Minimum
  Maximum

The resulting summary is stored in:

    results/stage3_rhrs/rhrs_diagnostics.json

This file provides a machine-readable check of the generated RHRS
distributions.

------------------------------------------------------------------------

# ▶️ 15. Reproduction

Run the component scripts first:

    python stage3_rhrs/hormonal_resilience.py
    python stage3_rhrs/physiological_resilience.py
    python stage3_rhrs/metabolic_resilience.py
    python stage3_rhrs/behavioral_resilience.py
    python stage3_rhrs/symptom_resilience.py

Then combine the five dimensions:

    python stage3_rhrs/compute_rhrs.py

Finally generate the diagnostics:

    python stage3_rhrs/rhrs_diagnostics.py

The execution order is therefore:

    clean_master_dataframe.csv
                │
                ├──────────────► HRS
                │
                ├──────────────► PRS
                │
                ├──────────────► MRS
                │
                ├──────────────► BRS
                │
                └──────────────► SRS
                                │
                                ▼
                         Weighted Aggregation
                                │
                                ▼
                              RHRS
                                │
                                ▼
                       Diagnostic Statistics

------------------------------------------------------------------------

# 📄 16. Connection to the Submitted Manuscript

Stage 3 corresponds primarily to **Section II-B --- Reproductive Health
Resilience Score (RHRS) Formulation** of the submitted manuscript.

The manuscript defines five resilience dimensions:

-   Hormonal Resilience Score (HRS)
-   Physiological Resilience Score (PRS)
-   Metabolic Resilience Score (MRS)
-   Behavioral Resilience Score (BRS)
-   Symptom Resilience Score (SRS)

These are subsequently combined into the overall RHRS.

The manuscript reports the following RHRS descriptive statistics:

  Score      Mean     Std     Min     Max
  ------- ------- ------- ------- -------
  HRS       50.01   17.89    1.77   98.33
  PRS       50.00   22.95    0.75   97.88
  MRS       49.99   22.24    0.02   99.80
  BRS       35.60   23.71    0.00   98.34
  SRS       49.99   16.38    2.14   91.80
  RHRS      47.12   10.24   15.88   81.05

These values are reported in Table II(c) of the submitted manuscript.

------------------------------------------------------------------------

# 🔗 17. Relationship to RHRS Validation

Stage 3 produces the scores that are subsequently evaluated in the
validation stage.

The manuscript evaluates RHRS through:

-   Internal consistency / reliability
-   Convergent validity
-   Known-group validation
-   Predictive validity

The validation implementation is therefore intentionally separated from
the score-construction implementation.

In particular, the calculation of **Cronbach's alpha is not performed by
this Stage 3 folder**. It belongs to the subsequent validation analysis.

This separation allows the reviewer to distinguish:

    RHRS FORMULATION
            ↓
    COMPONENT SCORES
            ↓
    OVERALL RHRS
            ↓
    VALIDATION

------------------------------------------------------------------------

# ⚠️ 18. Important Reproducibility Note

The scripts in this folder implement the computational scoring rules
used for the submitted study.

The repository therefore distinguishes between:

1.  **Implemented scoring rules** --- documented directly from the
    source code.
2.  **Reported study results** --- values presented in the submitted
    manuscript.
3.  **Fictional worked examples** --- included only to demonstrate the
    calculation flow.

The fictional example above must not be interpreted as participant data
or as a reported experimental result.

------------------------------------------------------------------------

# 🔐 19. Data Privacy

The original participant-level reproductive-health dataset is not
redistributed through this repository.

The scripts expect an authorized local copy of the processed input
dataset:

    data/processed/clean_master_dataframe.csv

Researchers should obtain the underlying mcPHASES data through the
applicable authorized access procedure and reproduce the computations
locally.

No participant-specific RHRS records, individual health profiles, or
real participant reports should be committed to the public repository
unless their release is explicitly permitted by the applicable
data-access conditions.

------------------------------------------------------------------------

# 🔄 20. Position in the WomenHealthAI Pipeline

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
              ├── HRS
              ├── PRS
              ├── MRS
              ├── BRS
              ├── SRS
              │
              ▼
            RHRS
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

> **Repository note:** Stage 3 provides the reproducible implementation
> of the RHRS formulation used in the submitted WomenHealthAI study. The
> component calculations, weighting coefficients, score directions,
> bounds, diagnostic outputs, and fictional worked example are
> documented here so that the RHRS construction can be independently
> inspected without exposing restricted participant-level data.
