def generate_recommendations(transactions):
    recommendations = []

    if not transactions:
        return ["Add some transactions to receive recommendations."]

    total_spending = 0

    for transaction in transactions:
        total_spending += float(transaction["amount"])

    if total_spending > 10000:
        recommendations.append(
            "Consider reviewing your expenses and reducing unnecessary spending."
        )
    else:
        recommendations.append(
            "Your current spending is within a manageable range."
        )

    recommendations.append(
        "Continue tracking your transactions regularly."
    )

    return recommendations