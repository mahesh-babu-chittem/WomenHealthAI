import pandas as pd
import json
from pathlib import Path

RESULTS_DIR = Path("results/stage3_rhrs")

df = pd.read_csv(
    "data/processed/clean_master_dataframe.csv"
)

hrs = pd.read_csv(
    RESULTS_DIR / "Table_5_HRS.csv"
)

prs = pd.read_csv(
    RESULTS_DIR / "Table_6_PRS.csv"
)

mrs = pd.read_csv(
    RESULTS_DIR / "Table_7_MRS.csv"
)

brs = pd.read_csv(
    RESULTS_DIR / "Table_8_BRS.csv"
)

srs = pd.read_csv(
    RESULTS_DIR / "Table_9_SRS.csv"
)

df["HRS"] = hrs["HRS"]
df["PRS"] = prs["PRS"]
df["MRS"] = mrs["MRS"]
df["BRS"] = brs["BRS"]
df["SRS"] = srs["SRS"]

df["RHRS"] = (
    0.25*df["HRS"]
    +
    0.25*df["PRS"]
    +
    0.15*df["MRS"]
    +
    0.20*df["BRS"]
    +
    0.15*df["SRS"]
)

df["RHRS"] = df["RHRS"].clip(0,100)

df.to_csv(
    "data/processed/rhrs_dataset.csv",
    index=False
)

df[
    [
        "id",
        "day_in_study",
        "HRS",
        "PRS",
        "MRS",
        "BRS",
        "SRS",
        "RHRS"
    ]
].to_csv(
    RESULTS_DIR / "Table_10_RHRS.csv",
    index=False
)

summary = {
    "mean_rhrs":
        float(df["RHRS"].mean()),
    "std_rhrs":
        float(df["RHRS"].std()),
    "min_rhrs":
        float(df["RHRS"].min()),
    "max_rhrs":
        float(df["RHRS"].max())
}

with open(
    RESULTS_DIR / "rhrs_summary.json",
    "w"
) as f:
    json.dump(summary,f,indent=4)

print(summary)