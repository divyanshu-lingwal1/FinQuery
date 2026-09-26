import csv


def generate_report(transactions):
    total_spending = 0

    for transaction in transactions:
        total_spending += float(transaction["amount"])

    return {
        "total_spending": total_spending,
        "transaction_count": len(transactions)
    }


def export_transactions_to_csv(transactions, file_path):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "date",
                "description",
                "category",
                "amount"
            ]
        )

        writer.writeheader()
        writer.writerows(transactions)

    return file_path