from mcp.server.fastmcp import FastMCP
from utils.storage import add_expense, list_expenses
from utils.db import init_db

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



if __name__ == "__main__":
    init_db()
    mcp.run(transport="stdio")