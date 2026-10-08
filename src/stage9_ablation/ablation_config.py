ABLATIONS = {
    "FULL": {
        "label": "Full WomenHealthAI (TFT + all RHRS dimensions)",
        "type": "baseline",
        "removed_features": [],
        "target_mode": "full_rhrs",
        "equal_weights": False,
        "temporal_attention": True,
        "adaptive_variable_selection": True,
    },
    "WO_HRS": {
        "label": "w/o Hormonal Resilience (HRS)",
        "type": "rh_dimension",
        "removed_features": ["HRS"],
        "target_mode": "full_rhrs",
        "equal_weights": False,
        "temporal_attention": True,
        "adaptive_variable_selection": True,
    },
    "WO_PRS": {
        "label": "w/o Physiological Resilience (PRS)",
        "type": "rh_dimension",
        "removed_features": ["PRS"],
        "target_mode": "full_rhrs",
        "equal_weights": False,
        "temporal_attention": True,
        "adaptive_variable_selection": True,
    },
    "WO_MRS": {
        "label": "w/o Metabolic Resilience (MRS)",
        "type": "rh_dimension",
        "removed_features": ["MRS"],
        "target_mode": "full_rhrs",
        "equal_weights": False,
        "temporal_attention": True,
        "adaptive_variable_selection": True,
    },
    "WO_BRS": {
        "label": "w/o Behavioral Resilience (BRS)",
        "type": "rh_dimension",
        "removed_features": ["BRS"],
        "target_mode": "full_rhrs",
        "equal_weights": False,
        "temporal_attention": True,
        "adaptive_variable_selection": True,
    },
    "WO_SRS": {
        "label": "w/o Symptom Resilience (SRS)",
        "type": "rh_dimension",
        "removed_features": ["SRS"],
        "target_mode": "full_rhrs",
        "equal_weights": False,
        "temporal_attention": True,
        "adaptive_variable_selection": True,
    },
    "EQUAL_WEIGHT_RHRS": {
        "label": "Equal-weight RHRS",
        "type": "rh_weighting",
        "removed_features": [],
        "target_mode": "equal_weight_rhrs",
        "equal_weights": True,
        "temporal_attention": True,
        "adaptive_variable_selection": True,
    },
    "WO_TEMPORAL_ATTENTION": {
        "label": "w/o Temporal Attention",
        "type": "tft_component",
        "removed_features": [],
        "target_mode": "full_rhrs",
        "equal_weights": False,
        "temporal_attention": False,
        "adaptive_variable_selection": True,
    },
    "WO_ADAPTIVE_VARIABLE_SELECTION": {
        "label": "w/o Adaptive Variable Selection",
        "type": "tft_component",
        "removed_features": [],
        "target_mode": "full_rhrs",
        "equal_weights": False,
        "temporal_attention": True,
        "adaptive_variable_selection": False,
    },
}

RHRS_DIMENSIONS = ["HRS", "PRS", "MRS", "BRS", "SRS"]

ORIGINAL_WEIGHTS = {
    "HRS": 0.25,
    "PRS": 0.25,
    "MRS": 0.15,
    "BRS": 0.20,
    "SRS": 0.15,
}

EQUAL_WEIGHTS = {key: 0.20 for key in RHRS_DIMENSIONS}

BASE_FEATURES = [
    "HRS", "PRS", "MRS", "BRS", "SRS",
    "lh", "estrogen", "pdg", "mean_rmssd", "mean_lf", "mean_hf",
    "mean_glucose", "std_glucose", "resting_hr", "sleep_score",
    "deep_sleep", "stress_score",
]

HORIZONS = (7, 14)

RESULT_FILES = {
    7: "../results/stage9_ablation/WomenHealthAI_ablation_results_7day.json",
    14: "../results/stage9_ablation/WomenHealthAI_ablation_results_14day.json",
}


def get_weights(ablation_key):
    return dict(EQUAL_WEIGHTS if ABLATIONS[ablation_key]["equal_weights"] else ORIGINAL_WEIGHTS)


def get_selected_features(ablation_key):
    removed = set(ABLATIONS[ablation_key]["removed_features"])
    return [feature for feature in BASE_FEATURES if feature not in removed]
