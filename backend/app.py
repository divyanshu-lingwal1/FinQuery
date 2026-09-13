from flask import Flask, request
from flask_cors import CORS
from services.analysis import (
    get_total_spending,
    get_spending_by_category,
    get_highest_spending_category,
    get_average_transaction,
    get_all_transactions,
    add_transaction,
    delete_transaction,
    update_transaction,
    search_transactions,
    get_spending_by_date_range,
    get_monthly_spending
)
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "FinQuery-V2 Backend is Running!"


@app.route("/api/summary")
def summary():
    total = get_total_spending()
    categories = get_spending_by_category()
    highest = get_highest_spending_category()
    average = get_average_transaction()

    return {
        "total_spending": float(total),
        "highest_category": highest[0],
        "highest_category_amount": float(highest[1]),
        "average_transaction": float(average),
        "spending_by_category": [
            {
                "category": category,
                "amount": float(amount)
            }
            for category, amount in categories
        ]
    }
@app.route("/api/transactions")
def transactions():
    results = get_all_transactions()

    transaction_data = []

    for transaction in results:
        transaction_data.append({
            "id": transaction[0],
            "date": str(transaction[1]),
            "description": transaction[2],
            "category": transaction[3],
            "amount": float(transaction[4])
        })

    return {
        "transactions": transaction_data
    }

@app.route("/api/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json()

    date = data["date"]
    description = data["description"]
    category = data["category"]
    amount = data["amount"]

    add_transaction(date, description, category, amount)

    return {
        "message": "Transaction added successfully!"
    }

@app.route("/api/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction_api(transaction_id):
    delete_transaction(transaction_id)

    return {
        "message": "Transaction deleted successfully!"
    }

@app.route("/api/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction_api(transaction_id):
    data = request.get_json()

    date = data["date"]
    description = data["description"]
    category = data["category"]
    amount = data["amount"]

    update_transaction(
        transaction_id,
        date,
        description,
        category,
        amount
    )

    return {
        "message": "Transaction updated successfully!"
    }

@app.route("/api/transactions/search")
def search_transactions_api():
    keyword = request.args.get("keyword", "")

    results = search_transactions(keyword)

    transaction_data = []

    for transaction in results:
        transaction_data.append({
            "id": transaction[0],
            "date": str(transaction[1]),
            "description": transaction[2],
            "category": transaction[3],
            "amount": float(transaction[4])
        })

    return {
        "transactions": transaction_data
    }

@app.route("/api/transactions/date-range")
def date_range_analysis():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    total = get_spending_by_date_range(start_date, end_date)

    if total is None:
        total = 0

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_spending": float(total)
    }

@app.route("/api/transactions/monthly")
def monthly_spending():
    results = get_monthly_spending()

    monthly_data = []

    for year, month, total in results:
        monthly_data.append({
            "year": year,
            "month": month,
            "total_spending": float(total)
        })

    return {
        "monthly_spending": monthly_data
    }

if __name__ == "__main__":
    app.run(debug=True)