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

def get_total_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    conn.close()

    return {
        "total_expenses": total if total is not None else 0
    }

def get_expenses_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        WHERE category = ?
    """, (category,))

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

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    if deleted:
        return {"message": f"Expense with ID {expense_id} deleted successfully."}
    else:
        return {"message": f"No expense found with ID {expense_id}."}


def update_expense(expense_id, amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET amount = ?, category = ?, description = ?, date = ?
        WHERE id = ?
    """, (amount, category, description, date, expense_id))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    if updated:
        return {
            "message": f"Expense with ID {expense_id} updated successfully."
        }
    else:
        return {
            "message": f"No expense found with ID {expense_id}."
        }
    
def set_budget(amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO budget(id, monthly_budget)
        VALUES (1, ?)
    """, (amount,))

    conn.commit()
    conn.close()

    return {"message": f"Monthly budget set to ₹{amount}"}

def get_budget():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT monthly_budget
        FROM budget
        WHERE id = 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None

def budget_status():
    budget = get_budget()

    if budget is None:
        return {"message": "No budget has been set."}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    spent = cursor.fetchone()[0] or 0

    conn.close()

    remaining = budget - spent

    percent = (spent / budget) * 100 if budget else 0

    return {
        "budget": budget,
        "spent": spent,
        "remaining": remaining,
        "used_percent": round(percent, 2)
    }