from db import get_connection
from utils import convert_date

def add_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    amount = float(input("Enter amount: "))
    category = input("Enter category: ").upper()
    description = input("Enter description: ").upper()
    date = convert_date(input("Enter date (DD-MM-YYYY): "))

    cursor.execute("SELECT MAX(local_id) FROM expenses WHERE user_id=%s", (user_id,))
    last_id = cursor.fetchone()[0]
    local_id = 1 if last_id is None else last_id + 1

    cursor.execute("""
        INSERT INTO expenses (user_id, amount, category, description, date, local_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, amount, category, description, date, local_id))
    conn.commit()

    print("Expense added!\n")


def view_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT local_id, amount, category, description, date 
        FROM expenses WHERE user_id=%s ORDER BY local_id ASC
    """, (user_id,))

    for r in cursor.fetchall():
        print(f"ID: {r[0]} | Amount: ₹{r[1]} | Category: {r[2]} | Desc: {r[3]} | Date: {r[4]}")


def view_by_category(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    category = input("Enter category: ").upper()

    cursor.execute("""
        SELECT local_id, amount, category, description, date 
        FROM expenses WHERE user_id=%s AND category=%s
    """, (user_id, category))

    rows = cursor.fetchall()
    if not rows:
        print("No expenses found.\n")
        return

    for r in rows:
        print(f"ID: {r[0]} | Amount: ₹{r[1]} | Desc: {r[3]} | Date: {r[4]}")


def view_by_description(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    keyword = input("Search text: ").upper()

    cursor.execute("""
        SELECT local_id, amount, category, description, date 
        FROM expenses WHERE user_id=%s AND description LIKE %s
    """, (user_id, "%" + keyword + "%"))

    rows = cursor.fetchall()
    if not rows:
        print("No expenses found.\n")
        return

    for r in rows:
        print(f"ID: {r[0]} | Amount: ₹{r[1]} | Category: {r[2]} | Desc: {r[3]} | Date: {r[4]}")


def delete_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    local_id = input("Enter expense ID to delete: ")

    cursor.execute("DELETE FROM expenses WHERE user_id=%s AND local_id=%s",
                   (user_id, local_id))
    conn.commit()

    print("Expense deleted!\n")


def update_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    local_id = input("Enter ID to update: ")
    amount = float(input("New amount: "))
    category = input("New category: ").upper()
    description = input("New description: ").upper()
    date = convert_date(input("New date (DD-MM-YYYY): "))

    cursor.execute("""
        UPDATE expenses 
        SET amount=%s, category=%s, description=%s, date=%s
        WHERE user_id=%s AND local_id=%s
    """, (amount, category, description, date, user_id, local_id))
    conn.commit()

    print("Expense updated!\n")


def delete_account(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    confirm = input("Type YES to confirm account delete: ")

    if confirm != "YES":
        print("Cancelled.\n")
        return

    cursor.execute("DELETE FROM expenses WHERE user_id=%s", (user_id,))
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()

    print("Account deleted.\n")
    return "DELETED"
