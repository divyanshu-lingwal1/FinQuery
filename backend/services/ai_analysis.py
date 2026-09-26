def analyze_finances(transactions):
    total_spending = 0

    for transaction in transactions:
        total_spending += float(transaction["amount"])

    return {
        "total_spending": total_spending,
        "transaction_count": len(transactions)
    }