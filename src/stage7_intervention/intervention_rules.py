def generate_interventions(patient):

    recommendations = []

    # Sleep

    if patient["sleep_score"] < 60:

        recommendations.append(
            "Improve sleep hygiene and maintain a consistent sleep schedule."
        )

    # Stress

    if patient["stress_score"] > 70:

        recommendations.append(
            "Practice stress-reduction techniques such as meditation and breathing exercises."
        )

    # HRV

    if patient["mean_rmssd"] < 40:

        recommendations.append(
            "Increase recovery-focused activities and reduce excessive physical strain."
        )

    # Resting Heart Rate

    if patient["resting_hr"] > 75:

        recommendations.append(
            "Monitor cardiovascular health and increase moderate physical activity."
        )

    # Glucose

    if patient["mean_glucose"] > 110:

        recommendations.append(
            "Improve dietary regulation and glucose management."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "Maintain current lifestyle habits."
        )

    return recommendations