def normalize_amount(amount):
    amount = str(amount)

    amount = amount.replace(",", "")
    amount = amount.replace("₹", "")
    amount = amount.strip()

    return float(amount)

def normalize_text(text):
    text = str(text)

    text = " ".join(text.split())

    return text


from datetime import datetime


def normalize_date(date_value):
    date_value = str(date_value).strip()

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y"
    ]

    for date_format in formats:
        try:
            date_object = datetime.strptime(date_value, date_format)
            return date_object.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError("Invalid date format")

def normalize_category(category):
    category = str(category).strip()

    if not category:
        return "Uncategorized"

    return category

def normalize_transaction(transaction):
    return {
        "date": normalize_date(transaction["date"]),
        "description": normalize_text(transaction["description"]),
        "category": normalize_category(transaction["category"]),
        "amount": normalize_amount(transaction["amount"])
    }