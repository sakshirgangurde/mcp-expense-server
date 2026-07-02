from utils.db import get_connection


def expense_analytics():

    conn = get_connection()
    cursor = conn.cursor()

    # Total Expenses
    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
    """)
    total = cursor.fetchone()[0] or 0

    # Number of Transactions
    cursor.execute("""
        SELECT COUNT(*)
        FROM expenses
    """)
    transactions = cursor.fetchone()[0]

    # Average Expense
    cursor.execute("""
        SELECT AVG(amount)
        FROM expenses
    """)
    average = cursor.fetchone()[0] or 0

    # Highest Expense
    cursor.execute("""
        SELECT MAX(amount)
        FROM expenses
    """)
    highest = cursor.fetchone()[0] or 0

    # Lowest Expense
    cursor.execute("""
        SELECT MIN(amount)
        FROM expenses
    """)
    lowest = cursor.fetchone()[0] or 0

    # Highest Spending Category
    cursor.execute("""
        SELECT category,
               SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    if row:
        highest_category = row[0]
        highest_category_amount = row[1]
    else:
        highest_category = None
        highest_category_amount = 0

    conn.close()

    return {
        "total_expenses": round(total, 2),
        "transaction_count": transactions,
        "average_expense": round(average, 2),
        "highest_expense": highest,
        "lowest_expense": lowest,
        "highest_category": highest_category,
        "highest_category_amount": highest_category_amount
    }