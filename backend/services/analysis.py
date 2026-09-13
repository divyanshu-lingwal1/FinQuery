from database.db import get_connection


def get_total_spending():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions")

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result[0]


def get_spending_by_category():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC
    """)

    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results

def get_highest_spending_category():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result


def get_average_transaction():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT AVG(amount) FROM transactions")

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result[0]

def get_all_transactions():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, date, description, category, amount
        FROM transactions
        ORDER BY date ASC
    """)

    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results

def add_transaction(date, description, category, amount):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, description, category, amount)
        VALUES (%s, %s, %s, %s)
    """, (date, description, category, amount))

    db.commit()

    cursor.close()
    db.close()

    return True
def add_transaction(date, description, category, amount):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, description, category, amount)
        VALUES (%s, %s, %s, %s)
    """, (date, description, category, amount))

    db.commit()

    cursor.close()
    db.close()

    return True


def delete_transaction(transaction_id):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = %s",
        (transaction_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return True

def update_transaction(transaction_id, date, description, category, amount):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE transactions
        SET date = %s,
            description = %s,
            category = %s,
            amount = %s
        WHERE id = %s
    """, (date, description, category, amount, transaction_id))

    db.commit()

    cursor.close()
    db.close()

    return True

def search_transactions(keyword):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, date, description, category, amount
        FROM transactions
        WHERE description LIKE %s
           OR category LIKE %s
        ORDER BY date ASC
    """, (f"%{keyword}%", f"%{keyword}%"))

    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results

def get_spending_by_date_range(start_date, end_date):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE date BETWEEN %s AND %s
    """, (start_date, end_date))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result[0]

def get_monthly_spending():
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT YEAR(date) AS year,
               MONTH(date) AS month,
               SUM(amount) AS total
        FROM transactions
        GROUP BY YEAR(date), MONTH(date)
        ORDER BY year ASC, month ASC
    """)

    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results