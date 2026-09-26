def generate_insights(transactions):
    insights = []

    if not transactions:
        return ["No financial data available."]

    total_spending = 0

    for transaction in transactions:
        total_spending += float(transaction["amount"])

    if total_spending > 5000:
        insights.append("Your total spending is above ₹5,000.")

    if total_spending <= 5000:
        insights.append("Your spending is currently below ₹5,000.")

    insights.append(
        f"You have recorded {len(transactions)} transactions."
    )

    return insights