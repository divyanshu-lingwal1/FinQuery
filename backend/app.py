from services.import_preview import create_preview
from services.import_history import save_import_history
from datetime import date
from flask import Flask, request, session
from flask_cors import CORS
from importers.pdf_importer import read_pdf_file, parse_pdf_transactions
from importers.docx_importer import read_docx_file, parse_docx_transactions
from importers.csv_importer import read_csv_file
from importers.ocr_importer import read_image_file
from importers.qr_importer import read_qr_code
from services.analysis import import_transactions
from services.analysis import (
    get_total_spending,
    get_spending_by_category,
    get_highest_spending_category,
    get_average_transaction,
    get_all_transactions,
    add_transaction,
    delete_transaction,
    register_user,
    update_transaction,
    search_transactions,
    get_spending_by_date_range,
    get_monthly_spending,
    login_user,
    get_total_transactions
)
app = Flask(__name__)

app.secret_key = "finquery-secret-key"

@app.route("/api/import/preview", methods=["POST"])
def import_preview():
    if "user_id" not in session:
        return {
            "success": False,
            "message": "Please login first"
        }, 401

    data = request.get_json()

    if not data or "transactions" not in data:
        return {
            "success": False,
            "message": "No transactions provided"
        }, 400

    preview = create_preview(data["transactions"])

    return {
        "success": True,
        "preview": preview
    }

@app.route("/api/import/history")
def import_history():
    if "user_id" not in session:
        return {
            "success": False,
            "message": "Please login first"
        }, 401

    from database.db import get_connection

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, file_type, record_count, imported_at
        FROM import_history
        WHERE user_id = %s
        ORDER BY imported_at DESC
    """, (session["user_id"],))

    results = cursor.fetchall()

    cursor.close()
    db.close()

    history = []

    for row in results:
        history.append({
            "id": row[0],
            "file_type": row[1],
            "record_count": row[2],
            "imported_at": str(row[3])
        })

    return {
        "success": True,
        "history": history
    }

@app.route("/api/import/csv", methods=["POST"])
def import_csv():
    if "user_id" not in session:
        return {"success": False, "message": "Please login first"}, 401

    if "file" not in request.files:
        return {"success": False, "message": "No file uploaded"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"success": False, "message": "No file selected"}, 400

    if not file.filename.lower().endswith(".csv"):
        return {"success": False, "message": "Only CSV files are allowed"}, 400

    file_path = "temp_import.csv"
    file.save(file_path)

    try:
        transactions = read_csv_file(file_path)

        import_transactions(
            transactions,
            session["user_id"]
        )

        return {
            "success": True,
            "message": "CSV transactions imported successfully!",
            "count": len(transactions)
        }

    except ValueError as error:
        return {
            "success": False,
            "message": str(error)
        }, 400

@app.route("/api/import/pdf", methods=["POST"])
def import_pdf():
    if "user_id" not in session:
        return {"success": False, "message": "Please login first"}, 401

    if "file" not in request.files:
        return {"success": False, "message": "No file uploaded"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"success": False, "message": "No file selected"}, 400

    if not file.filename.lower().endswith(".pdf"):
        return {"success": False, "message": "Only PDF files are allowed"}, 400

    if not file.filename.lower().endswith(".pdf"):
        return {"success": False, "message": "Only PDF files are allowed"}, 400

    file_path = "temp_import.pdf"
    file.save(file_path)

    try:
        text = read_pdf_file(file_path)

        transactions = parse_pdf_transactions(text)

        import_transactions(
            transactions,
            session["user_id"]
        )

        print("\n========== PDF TRANSACTIONS ==========")
        print(transactions)
        print("========== END PDF TRANSACTIONS ==========\n")

        return {
            "success": True,
            "message": "PDF transactions imported successfully!",
            "count": len(transactions),
            "transactions": transactions
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }, 400

@app.route("/api/import/docx", methods=["POST"])
def import_docx():

    if "user_id" not in session:
        return {
            "success": False,
            "message": "Please login first"
        }, 401

    if "file" not in request.files:
        return {
            "success": False,
            "message": "No file uploaded"
        }, 400

    file = request.files["file"]

    if file.filename == "":
        return {
            "success": False,
            "message": "No file selected"
        }, 400

    if not file.filename.lower().endswith(".docx"):
        return {
            "success": False,
            "message": "Only DOCX files are allowed"
        }, 400

    file_path = "temp_import.docx"
    file.save(file_path)

    try:

        text = read_docx_file(file_path)

        transactions = parse_docx_transactions(text)

        import_transactions(
            transactions,
            session["user_id"]
        )

        print("\n========== DOCX TRANSACTIONS ==========")
        print(transactions)
        print("========== END DOCX TRANSACTIONS ==========\n")

        return {
            "success": True,
            "message": "DOCX transactions imported successfully!",
            "count": len(transactions),
            "transactions": transactions
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }, 400

@app.route("/api/import/image", methods=["POST"])
def import_image():
    if "user_id" not in session:
        return {"success": False, "message": "Please login first"}, 401

    if "file" not in request.files:
        return {"success": False, "message": "No file uploaded"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"success": False, "message": "No file selected"}, 400

    allowed_extensions = [".png", ".jpg", ".jpeg"]

    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        return {
            "success": False,
            "message": "Only PNG, JPG and JPEG files are allowed"
        }, 400

    file_path = "temp_import_image"

    file.save(file_path)

    try:
        text = read_image_file(file_path)

        return {
            "success": True,
            "text": text
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }, 400

@app.route("/api/import/qr", methods=["POST"])
def import_qr():
    if "user_id" not in session:
        return {"success": False, "message": "Please login first"}, 401

    if "file" not in request.files:
        return {"success": False, "message": "No file uploaded"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"success": False, "message": "No file selected"}, 400

    allowed_extensions = [".png", ".jpg", ".jpeg"]

    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        return {
            "success": False,
            "message": "Only PNG, JPG and JPEG files are allowed"
        }, 400

    file_path = "temp_import_qr"

    file.save(file_path)

    try:
        data = read_qr_code(file_path)

        return {
            "success": True,
            "data": data
        }

    except ValueError as error:
        return {
            "success": False,
            "message": str(error)
        }, 400

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }, 400

CORS(
    app,
    supports_credentials=True,
    origins=["http://127.0.0.1:5500"]
)


@app.route("/")
def home():
    return "FinQuery-V2 Backend is Running!"


@app.route("/api/summary")
def summary():
    user_id = session["user_id"]

    total = get_total_spending(user_id)
    total_transactions = get_total_transactions(user_id)
    categories = get_spending_by_category(user_id)
    highest = get_highest_spending_category(user_id)
    average = get_average_transaction(user_id)
    
    return {
        "total_spending": float(total),
        "total_transactions": total_transactions,
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
    user_id = session["user_id"]

    results = get_all_transactions(user_id)

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

    user_id = session["user_id"]

    add_transaction(date, description, category, amount, user_id)

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
    user_id = session["user_id"]

    results = get_monthly_spending(user_id)

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

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = data["password"]

    register_user(name, email, password)

    return {
        "message": "User registered successfully!"
    }

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    user = login_user(email, password)

    if user:
        session["user_id"] = user[0]
        print("Logged in user ID:", session["user_id"])

        return {
            "success": True,
            "message": "Login successful!",
            "user": {
                "id": user[0],
                "name": user[1],
                "email": user[2]
            }
        }

    return {
        "success": False,
        "message": "Invalid email or password"
    }, 401

@app.route("/api/me")
def current_user():
    if "user_id" not in session:
        return {
            "logged_in": False
        }, 401

    return {
        "logged_in": True,
        "user_id": session["user_id"]
    }


if __name__ == "__main__":
    app.run(debug=True)