"""Supported ablations for the native PyTorch Forecasting TFT."""
RHRS_DIMENSIONS = ["HRS", "PRS", "MRS", "BRS", "SRS"]
ORIGINAL_WEIGHTS = {"HRS": 0.25, "PRS": 0.25, "MRS": 0.15, "BRS": 0.20, "SRS": 0.15}
EQUAL_WEIGHTS = {name: 0.20 for name in RHRS_DIMENSIONS}
ABLATIONS = {
    "FULL": {"label": "Native TFT — all RHRS dimensions", "type": "baseline", "removed_features": [], "target_mode": "original_rhrs"},
    "WO_HRS": {"label": "Native TFT — HRS removed from inputs", "type": "input_dimension_removal", "removed_features": ["HRS"], "target_mode": "original_rhrs"},
    "WO_PRS": {"label": "Native TFT — PRS removed from inputs", "type": "input_dimension_removal", "removed_features": ["PRS"], "target_mode": "original_rhrs"},
    "WO_MRS": {"label": "Native TFT — MRS removed from inputs", "type": "input_dimension_removal", "removed_features": ["MRS"], "target_mode": "original_rhrs"},
    "WO_BRS": {"label": "Native TFT — BRS removed from inputs", "type": "input_dimension_removal", "removed_features": ["BRS"], "target_mode": "original_rhrs"},
    "WO_SRS": {"label": "Native TFT — SRS removed from inputs", "type": "input_dimension_removal", "removed_features": ["SRS"], "target_mode": "original_rhrs"},
    "EQUAL_WEIGHT_RHRS": {"label": "Native TFT — equal-weight RHRS target", "type": "target_weighting_sensitivity", "removed_features": [], "target_mode": "equal_weight_rhrs"},
}
HORIZONS = (7, 14)
RESULT_FILES = {7: "WomenHealthAI_ablation_results_7day.json", 14: "WomenHealthAI_ablation_results_14day.json"}
FEATURE_COLUMNS = [
    "lh", "estrogen", "pdg", "mean_rmssd", "mean_lf", "mean_hf", "resting_hr",
    "mean_glucose", "std_glucose", "sleep_score", "deep_sleep", "stress_score",
    "headaches", "cramps", "fatigue", "foodcravings", "bloating",
    "HRS", "PRS", "MRS", "BRS", "SRS",
]
def get_features(ablation_key):
    removed = set(ABLATIONS[ablation_key]["removed_features"])
    return [c for c in FEATURE_COLUMNS if c not in removed]
