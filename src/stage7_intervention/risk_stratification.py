import pandas as pd

def classify_risk(rhrs):

    if rhrs >= 70:
        return "High Resilience"

    elif rhrs >= 50:
        return "Moderate Resilience"

    elif rhrs >= 30:
        return "Low Resilience"

    else:
        return "Critical"