import csv
from openpyxl import Workbook
from db import get_connection

def report_csv(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT local_id, amount, category, description, date FROM expenses WHERE user_id=%s",
                   (user_id,))
    rows = cursor.fetchall()

    if not rows:
        print("No data.\n")
        return

    filename = f"{user_id}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Amount", "Category", "Description", "Date"])
        writer.writerows(rows)

    print("CSV exported.\n")


def report_excel(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT local_id, amount, category, description, date FROM expenses WHERE user_id=%s",
                   (user_id,))
    rows = cursor.fetchall()

    if not rows:
        print("No data.\n")
        return

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Expenses"

    sheet.append(["ID", "Amount", "Category", "Description", "Date"])
    for r in rows:
        sheet.append(r)

    filename = f"{user_id}.xlsx"
    workbook.save(filename)

    print("Excel exported.\n")


def report_monthly(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    month = int(input("Month (MM): "))
    year = int(input("Year (YYYY): "))

    cursor.execute("""
        SELECT local_id, amount, category, description, date 
        FROM expenses 
        WHERE user_id=%s AND MONTH(date)=%s AND YEAR(date)=%s
    """, (user_id, month, year))

    rows = cursor.fetchall()
    if not rows:
        print("No records.\n")
        return

    for r in rows:
        print(f"ID: {r[0]} | ₹{r[1]} | {r[2]} | {r[3]} | {r[4]}")
