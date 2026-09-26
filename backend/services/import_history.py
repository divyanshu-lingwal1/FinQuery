from database.db import get_connection


def save_import_history(user_id, file_type, record_count):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO import_history
        (user_id, file_type, record_count)
        VALUES (%s, %s, %s)
    """, (
        user_id,
        file_type,
        record_count
    ))

    db.commit()

    cursor.close()
    db.close()