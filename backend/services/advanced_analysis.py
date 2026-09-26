def calculate_monthly_trend(transactions):
    monthly_totals = {}

    for transaction in transactions:
        date = transaction["date"]
        amount = float(transaction["amount"])

        month = date[:7]

        if month not in monthly_totals:
            monthly_totals[month] = 0

        monthly_totals[month] += amount

    return monthly_totals

def calculate_category_totals(transactions):
    category_totals = {}

    for transaction in transactions:
        category = transaction["category"]
        amount = float(transaction["amount"])

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += amount

    return category_totals

def generate_dashboard_insights(transactions):
    total_spending = 0
    highest_expense = 0

    for transaction in transactions:
        amount = float(transaction["amount"])

        total_spending += amount

        if amount > highest_expense:
            highest_expense = amount

    return {
        "total_spending": total_spending,
        "highest_expense": highest_expense,
        "transaction_count": len(transactions)
    }