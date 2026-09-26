def parse_transaction(text):
    lines = text.strip().splitlines()

    transactions = []

    for line in lines:
        parts = line.split()

        if len(parts) < 4:
            continue

        if parts[0].lower() == "date":
            continue

        date = parts[0]
        amount = parts[-1]
        category = parts[-2]
        description = " ".join(parts[1:-2])

        transaction = {
            "date": date,
            "description": description,
            "category": category,
            "amount": amount
        }

        transactions.append(transaction)

    return transactions