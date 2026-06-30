from openpyxl import Workbook
from utils.db import get_connection
import os
import traceback


def export_expenses_to_excel():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
        """)

        rows = cursor.fetchall()

        conn.close()

        workbook = Workbook()

        sheet = workbook.active
        sheet.title = "Expenses"

        sheet.append([
            "ID",
            "Amount",
            "Category",
            "Description",
            "Date"
        ])

        for row in rows:
            sheet.append(row)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        EXPORT_FOLDER = os.path.join(BASE_DIR, "..", "exports")
        EXPORT_FOLDER = os.path.normpath(EXPORT_FOLDER)

        os.makedirs(EXPORT_FOLDER, exist_ok=True)

        file_path = os.path.join(EXPORT_FOLDER, "expenses.xlsx")

        workbook.save(file_path)


        return {
            "message": "HELLO FROM MY MCP SERVER",
            "file": file_path
        }

    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }





