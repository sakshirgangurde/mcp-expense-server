import streamlit as st
import pandas as pd
from utils.db import get_connection
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Expense Tracker Dashboard",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Expense Tracker Dashboard")

# Connect to SQLite
conn = get_connection()

# Load Expenses
expenses_df = pd.read_sql_query("SELECT * FROM expenses", conn)
category_df = (expenses_df.groupby("category")["amount"].sum().reset_index())

# Total Expenses
total_expenses = expenses_df["amount"].sum()

# Number of Transactions
transactions = len(expenses_df)

# Monthly Budget
budget_query = pd.read_sql_query(
    "SELECT monthly_budget FROM budget WHERE id = 1",
    conn
)

if not budget_query.empty:
    monthly_budget = budget_query.iloc[0]["monthly_budget"]
else:
    monthly_budget = 0

remaining_budget = monthly_budget - total_expenses

conn.close()

# Metric Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💸 Total Expenses", f"₹{total_expenses:,.2f}")

with col2:
    st.metric("💰 Monthly Budget", f"₹{monthly_budget:,.2f}")

with col3:
    st.metric("✅ Remaining Budget", f"₹{remaining_budget:,.2f}")

with col4:
    st.metric("📄 Transactions", transactions)

st.divider()

st.subheader("🥧 Expense Distribution")

pie_chart = px.pie(
    category_df,
    names="category",
    values="amount",
    hole=0.4,
    title="Expenses by Category"
)

st.plotly_chart(pie_chart, use_container_width=True)

st.subheader("📊 Category-wise Expenses")

bar_chart = px.bar(
    category_df,
    x="category",
    y="amount",
    text="amount",
    title="Total Spending per Category"
)

st.plotly_chart(bar_chart, use_container_width=True)

st.divider()

st.subheader("📋 Expense Records")

st.dataframe(expenses_df, use_container_width=True)