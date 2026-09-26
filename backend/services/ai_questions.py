def answer_financial_question(question, transactions):
    question = question.lower()

    if "total" in question or "spending" in question:
        total = 0

        for transaction in transactions:
            total += float(transaction["amount"])

        return f"Your total spending is ₹{total:.2f}."

    if "transaction" in question:
        return f"You have {len(transactions)} transactions."

    return "I could not understand the financial question."