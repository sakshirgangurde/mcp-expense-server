from mcp.server.fastmcp import FastMCP
from utils.storage import add_expense, list_expenses, get_total_expenses, get_expenses_by_category, delete_expense, update_expense, set_budget, budget_status
from utils.db import init_db
from utils.export import export_expenses_to_excel
from utils.pdf_report import generate_monthly_report

mcp = FastMCP("Expense Tracker MCP")

@mcp.tool()
def add_new_expense(
    amount: float,
    category: str,
    description: str,
    date: str,
):
    return add_expense(amount, category, description, date)


@mcp.tool()
def show_expenses():
    return list_expenses()

@mcp.tool()
def show_total_expenses():
    return get_total_expenses()

@mcp.tool()
def show_expenses_by_category(category: str):
    return get_expenses_by_category(category)

@mcp.tool()
def delete_expense_by_id(expense_id: int):
    return delete_expense(expense_id)

@mcp.tool()
def update_existing_expense(
    expense_id: int,
    amount: float,
    category: str,
    description: str,
    date: str,
):
    return update_expense(
        expense_id,
        amount,
        category,
        description,
        date,
    )

@mcp.tool()
def set_monthly_budget(amount: float):
    return set_budget(amount)


@mcp.tool()
def show_budget_status():
    return budget_status()

@mcp.tool()
def export_expenses():
    return export_expenses_to_excel()

@mcp.tool()
def export_monthly_report():
    return generate_monthly_report()

if __name__ == "__main__":
    init_db()
    mcp.run(transport="stdio")