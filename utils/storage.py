from utils.db import get_connection

def add_expense(amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, date))

    conn.commit()

    expense_id = cursor.lastrowid
    conn.close()

    return {
        "id": expense_id,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

def list_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "amount": r[1],
            "category": r[2],
            "description": r[3],
            "date": r[4]
        }
        for r in rows
    ]
