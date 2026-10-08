def generate_resilience_interventions(patient):

    interventions = []

    # =====================================
    # HRS
    # =====================================

    if patient["HRS"] < 50:

        interventions.append(
            "Hormonal resilience is reduced. Monitor hormonal fluctuations and consider endocrine evaluation."
        )

    # =====================================
    # PRS
    # =====================================

    if patient["PRS"] < 50:

        interventions.append(
            "Psychological resilience is low. Stress management and mental wellness support are recommended."
        )

    # =====================================
    # MRS
    # =====================================

    if patient["MRS"] < 50:

        interventions.append(
            "Metabolic resilience is reduced. Improve nutrition, glucose regulation, and physical activity."
        )

    # =====================================
    # BRS
    # =====================================

    if patient["BRS"] < 50:

        interventions.append(
            "Behavioral resilience is low. Improve sleep hygiene and daily health routines."
        )

    # =====================================
    # SRS
    # =====================================

    if patient["SRS"] < 50:

        interventions.append(
            "Symptom resilience is reduced. Increased symptom monitoring is recommended."
        )

    # =====================================
    # RHRS
    # =====================================

    if patient["RHRS"] < 40:

        interventions.append(
            "Overall resilience is low. Comprehensive intervention and closer monitoring are recommended."
        )

    if len(interventions) == 0:

        interventions.append(
            "Current resilience profile is stable. Maintain present lifestyle and monitoring practices."
        )

    return interventions