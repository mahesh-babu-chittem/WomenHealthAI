import numpy as np

from scipy.stats import (
    pearsonr,
    spearmanr,
    kendalltau
)

from sklearn.metrics import (

    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,

    median_absolute_error,
    max_error,

    r2_score,
    explained_variance_score,

    accuracy_score,
    precision_score,
    recall_score,
    f1_score,

    balanced_accuracy_score,

    matthews_corrcoef,

    cohen_kappa_score,

    confusion_matrix,

    roc_auc_score,

    average_precision_score
)

# ==================================================
# SMAPE
# ==================================================

def smape(y_true, y_pred):

    denominator = (
        np.abs(y_true)
        +
        np.abs(y_pred)
    ) / 2

    mask = denominator != 0

    return np.mean(
        np.abs(
            y_true[mask]
            -
            y_pred[mask]
        )
        /
        denominator[mask]
    ) * 100


# ==================================================
# TREND LABELS
# ==================================================

def create_trend_labels(values):

    labels = []

    for i in range(1, len(values)):

        diff = values[i] - values[i-1]

        if diff > 0:

            labels.append(1)

        elif diff < 0:

            labels.append(-1)

        else:

            labels.append(0)

    return np.array(labels)


# ==================================================
# RHRS RISK LABELS
# ==================================================

def create_risk_labels(values):

    labels = []

    for v in values:

        if v < 40:

            labels.append(0)

        elif v < 70:

            labels.append(1)

        else:

            labels.append(2)

    return np.array(labels)


# ==================================================
# COHEN D
# ==================================================

def cohens_d(y_true, y_pred):

    pooled_std = np.sqrt(

        (
            np.var(y_true, ddof=1)
            +
            np.var(y_pred, ddof=1)
        ) / 2

    )

    if pooled_std == 0:

        return 0

    return (

        np.mean(y_true)
        -
        np.mean(y_pred)

    ) / pooled_std


# ==================================================
# MAIN METRICS
# ==================================================

def compute_all_metrics(
    y_true,
    y_pred
):

    metrics = {}

    # =====================================
    # REGRESSION
    # =====================================

    metrics["MAE"] = float(
        mean_absolute_error(
            y_true,
            y_pred
        )
    )

    metrics["MSE"] = float(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    metrics["RMSE"] = float(
        np.sqrt(
            metrics["MSE"]
        )
    )

    metrics["MAPE"] = float(
        mean_absolute_percentage_error(
            y_true,
            y_pred
        ) * 100
    )

    metrics["SMAPE"] = float(
        smape(
            y_true,
            y_pred
        )
    )

    metrics["MedAE"] = float(
        median_absolute_error(
            y_true,
            y_pred
        )
    )

    metrics["MaxError"] = float(
        max_error(
            y_true,
            y_pred
        )
    )

    metrics["R2"] = float(
        r2_score(
            y_true,
            y_pred
        )
    )

    metrics["ExplainedVariance"] = float(
        explained_variance_score(
            y_true,
            y_pred
        )
    )

    # =====================================
    # CORRELATION
    # =====================================

    metrics["Pearson"] = float(
        pearsonr(
            y_true,
            y_pred
        )[0]
    )

    metrics["Spearman"] = float(
        spearmanr(
            y_true,
            y_pred
        )[0]
    )

    metrics["KendallTau"] = float(
        kendalltau(
            y_true,
            y_pred
        )[0]
    )

    # =====================================
    # TREND METRICS
    # =====================================

    true_trend = create_trend_labels(
        y_true
    )

    pred_trend = create_trend_labels(
        y_pred
    )

    metrics["TrendAccuracy"] = float(
        accuracy_score(
            true_trend,
            pred_trend
        )
    )

    metrics["TrendPrecision"] = float(
        precision_score(
            true_trend,
            pred_trend,
            average="macro",
            zero_division=0
        )
    )

    metrics["TrendRecall"] = float(
        recall_score(
            true_trend,
            pred_trend,
            average="macro",
            zero_division=0
        )
    )

    metrics["TrendF1"] = float(
        f1_score(
            true_trend,
            pred_trend,
            average="macro",
            zero_division=0
        )
    )

    # =====================================
    # RISK CLASSIFICATION
    # =====================================

    y_true_cls = create_risk_labels(
        y_true
    )

    y_pred_cls = create_risk_labels(
        y_pred
    )

    metrics["Accuracy"] = float(
        accuracy_score(
            y_true_cls,
            y_pred_cls
        )
    )

    metrics["Precision"] = float(
        precision_score(
            y_true_cls,
            y_pred_cls,
            average="macro",
            zero_division=0
        )
    )

    metrics["Recall"] = float(
        recall_score(
            y_true_cls,
            y_pred_cls,
            average="macro",
            zero_division=0
        )
    )

    metrics["F1"] = float(
        f1_score(
            y_true_cls,
            y_pred_cls,
            average="macro",
            zero_division=0
        )
    )

    metrics["BalancedAccuracy"] = float(
        balanced_accuracy_score(
            y_true_cls,
            y_pred_cls
        )
    )

    metrics["MCC"] = float(
        matthews_corrcoef(
            y_true_cls,
            y_pred_cls
        )
    )

    metrics["CohenKappa"] = float(
        cohen_kappa_score(
            y_true_cls,
            y_pred_cls
        )
    )

    # =====================================
    # CONFUSION MATRIX
    # =====================================

    cm = confusion_matrix(
        y_true_cls,
        y_pred_cls,
        labels=[0,1,2]
    )

    metrics["TPR"] = float(
        np.trace(cm)
        /
        np.sum(cm)
    )

    metrics["FPR"] = float(
        1 -
        metrics["TPR"]
    )

    metrics["TNR"] = float(
        1 -
        metrics["FPR"]
    )

    metrics["FNR"] = float(
        1 -
        metrics["TPR"]
    )

    # =====================================
    # AUC
    # =====================================

    try:

        metrics["ROC_AUC"] = float(
            roc_auc_score(
                y_true_cls,
                y_pred_cls,
                multi_class="ovr"
            )
        )

    except:

        metrics["ROC_AUC"] = np.nan

    try:

        metrics["PR_AUC"] = float(
            average_precision_score(
                y_true_cls,
                y_pred_cls
            )
        )

    except:

        metrics["PR_AUC"] = np.nan

    # =====================================
    # COHEN D
    # =====================================

    metrics["CohensD"] = float(
        cohens_d(
            y_true,
            y_pred
        )
    )

    return metrics