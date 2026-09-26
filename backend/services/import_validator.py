from datetime import datetime

def validate_transaction(transaction):
    errors = []

    required_fields = [
        "date",
        "description",
        "category",
        "amount"
    ]

    for field in required_fields:
        if field not in transaction or transaction[field] in ("", None):
            errors.append(f"Missing {field}")

    if "amount" in transaction and transaction["amount"] not in ("", None):
        try:
            float(transaction["amount"])
        except (ValueError, TypeError):
            errors.append("Invalid amount")

        if "date" in transaction and transaction["date"] not in ("", None):
            valid_date = False

            formats = [
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%d/%m/%Y"
            ]

            for date_format in formats:
                try:
                    datetime.strptime(str(transaction["date"]), date_format)
                    valid_date = True
                    break
                except ValueError:
                    continue

            if not valid_date:
                errors.append("Invalid date")

    return errors

def validate_transactions(transactions):
    valid_transactions = []
    errors = []

    for index, transaction in enumerate(transactions):
        transaction_errors = validate_transaction(transaction)

        if transaction_errors:
            errors.append({
                "row": index + 1,
                "errors": transaction_errors
            })
        else:
            valid_transactions.append(transaction)

    return {
        "valid_transactions": valid_transactions,
        "errors": errors
    }