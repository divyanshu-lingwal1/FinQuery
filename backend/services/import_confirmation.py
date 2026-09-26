from services.analysis import import_transactions


def confirm_import(transactions, user_id):
    import_transactions(transactions, user_id)

    return {
        "confirmed": True,
        "count": len(transactions),
        "transactions": transactions
    }