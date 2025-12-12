import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db import get_connection

def plot_category_spending(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
    """, (user_id,))

    rows = cursor.fetchall()
    if not rows:
        print("No expenses.\n")
        return

    df = pd.DataFrame(rows, columns=["Category", "Total"])

    print("1. Pie Chart\n2. Bar Graph")
    choice = input("Enter choice: ")

    if choice == "1":
        plt.pie(df["Total"], labels=df["Category"], autopct="%1.1f%%")
        plt.title("Spending Pie Chart")
        plt.show()

    elif choice == "2":
        sns.barplot(x="Category", y="Total", data=df)
        plt.title("Spending by Category")
        plt.show()
