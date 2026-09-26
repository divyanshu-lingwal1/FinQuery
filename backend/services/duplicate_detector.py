def find_duplicates(transactions):
    duplicates = []
    seen = set()

    for index, transaction in enumerate(transactions):
        key = (
            transaction["date"],
            transaction["description"],
            transaction["category"],
            transaction["amount"]
        )

        if key in seen:
            duplicates.append(index + 1)
        else:
            seen.add(key)

    return duplicates