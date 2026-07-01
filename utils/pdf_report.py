from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from utils.db import get_connection
import os
from datetime import datetime


def generate_monthly_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
    """)

    rows = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT monthly_budget
        FROM budget
        WHERE id = 1
    """)

    budget_row = cursor.fetchone()
    budget = budget_row[0] if budget_row else 0

    conn.close()

    remaining = budget - total

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    REPORT_FOLDER = os.path.join(BASE_DIR, "..", "reports")
    REPORT_FOLDER = os.path.normpath(REPORT_FOLDER)

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    filename = f"Expense_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    file_path = os.path.join(REPORT_FOLDER, filename)

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>Expense Tracker Monthly Report</b>", styles["Title"])
    )

    elements.append(
        Paragraph(f"Generated : {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                  styles["Normal"])
    )

    elements.append(
        Paragraph(f"<br/>Total Expenses : ₹{total}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Monthly Budget : ₹{budget}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Remaining Budget : ₹{remaining}", styles["Normal"])
    )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    table_data = [
        ["ID", "Amount", "Category", "Description", "Date"]
    ]

    for row in rows:
        table_data.append(list(row))

    table = Table(table_data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("ALIGN", (0, 0), (-1, -1), "CENTER")

    ]))

    elements.append(table)

    doc.build(elements)

    return {
        "message": "Monthly PDF report generated successfully.",
        "file": file_path
    }