import mysql.connector
from datetime import datetime
import csv
import os
from openpyxl import Workbook
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



conn =mysql.connector.connect(
        host="localhost",
        user="root",
        password="ChiragSamaiya",      
        database="expense_tracker"
    )

cursor = conn.cursor()

def register():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                       (username, password))
    conn.commit()
    print("Registration successful!\n")


def login():
     username = input("Enter username: ")
     password = input("Enter password: ")

     cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s",
                   (username, password))
     result = cursor.fetchone()

     if result:
        print("\nLogin successful!")
        return result[0]
     else:
        print("Invalid credentials.\n")
        return None

def convert_date(date_input):
    d = datetime.strptime(date_input, "%d-%m-%Y")   
    return d.strftime("%Y-%m-%d") 


def add_expense(user_id):
    amount = float(input("Enter amount: "))
    category = input("Enter category: ").upper()
    description = input("Enter description: ").upper()
    date_input = input("Enter date (DD-MM-YYYY): ")
    date = convert_date(date_input)

    if not date:
        return 
    
    cursor.execute("SELECT MAX(local_id) FROM expenses WHERE user_id = %s", (user_id,))
    last_local_id = cursor.fetchone()[0]

    if last_local_id is None:
        local_id = 1
    else:
        local_id = last_local_id + 1


    cursor.execute("""INSERT INTO expenses (user_id, amount, category, description, date,local_id)
                      VALUES (%s, %s, %s, %s, %s,%s)""",
                   (user_id, amount, category, description, date,local_id))
    conn.commit()

    print("Expense added successfully\n")


def view_expenses(user_id):
     cursor.execute("SELECT local_id, amount, category, description, date FROM expenses WHERE user_id=%s   ORDER BY local_id ASC ",
                   (user_id,))
     rows = cursor.fetchall()

    
     for r in rows:
        print(f"ID: {r[0]} | Amount: ₹{r[1]} | Category: {r[2]} | Desc: {r[3]} | Date: {r[4]}")

def view_by_category(user_id):
    category = input("Enter category to filter: ").upper()

    cursor.execute("""
        SELECT local_id, amount, category, description, date 
        FROM expenses 
        WHERE user_id = %s AND category = %s
    """, (user_id, category))

    rows = cursor.fetchall()

    if not rows:
        print(f"No expenses found for category: {category}\n")
        return

    print(f"\nExpenses under category: {category}\n")
    for r in rows:
        print(f"ID: {r[0]} | Amount: ₹{r[1]} | Desc: {r[3]} | Date: {r[4]}")
    print()



def view_expense_by_description(user_id):
    keyword = input("Enter text to search in description: ").upper()

    cursor.execute("""
        SELECT local_id, amount, category, description, date
        FROM expenses
        WHERE user_id = %s AND description LIKE %s
        ORDER BY date ASC
    """, (user_id, "%" + keyword + "%"))

    rows = cursor.fetchall()

    if not rows:
        print(f"No expenses found containing: {keyword}\n")
        return

    print(f"\nExpenses containing '{keyword}':\n")
    for r in rows:
        print(f"ID: {r[0]} | Amount: ₹{r[1]} | Category: {r[2]} | Desc: {r[3]} | Date: {r[4]}")
    print()

def delete_expense(user_id):
    local_id = input("Enter expense ID to delete: ")

    cursor.execute("DELETE FROM expenses WHERE user_id=%s AND local_id=%s",
                   (user_id,local_id))
    conn.commit()

    print("Expense deleted!\n")


def update_expense(user_id):
    local_id = input("Enter expense ID to update: ")

    amount = float(input("New amount: "))
    category = input("New category: ").upper()
    description = input("New description: ").upper()
    date_input = input("Enter date (DD-MM-YYYY): ")
    date = convert_date(date_input)

    if not date:
        return  


    cursor.execute("""UPDATE expenses
                      SET amount=%s, category=%s, description=%s, date=%s
                      WHERE  user_id=%s AND local_id=%s""",
                     (amount, category, description, date,  user_id,local_id))
    conn.commit()

    print("Expense updated\n")

def report_csv(user_id):
  
   cursor.execute("""SELECT local_id, amount, category, description, date FROM expenses WHERE user_id = %s
""",(user_id,))
   
   rows= cursor.fetchall()

   if not rows:
        print("No expenses found to export.\n")
        return

   filename = f"{user_id}.csv"

   with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow(["ID", "Amount", "Category", "Description", "Date"])
        
        for row in rows:
            writer.writerow(row)

   print(f"CSV exported successfully → {filename}\n")
  
from openpyxl import Workbook

def report_excel(user_id):
    cursor.execute("SELECT local_id, amount, category, description, date FROM expenses WHERE user_id = %s",
                   (user_id,))
    rows = cursor.fetchall()

    if not rows:
        print("No expenses found to export.\n")
        return

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Expenses"

    sheet.append(["ID", "Amount", "Category", "Description", "Date"])

    for row in rows:
        sheet.append(row)

    filename = f"{user_id}.xlsx"
    workbook.save(filename)

    print(f"Excel exported successfully → {filename}\n")

def report_monthly(user_id):
    month = int(input("Enter month (MM) :"))
    year = int(input("Enter Year (YYYY) : "))

    cursor.execute("""SELECT local_id, amount, category, description,date  FROM expenses WHERE user_id=%s AND MONTH(date)=%s  AND YEAR(date) = %s""",(user_id,month,year))

    rows = cursor.fetchall()

    if not rows:
        print("\nNo expenses found for this month.\n")
        return

    print(f"\nExpenses for {month}-{year}:\n")
    for r in rows:
        print(f"ID: {r[0]} | Amount: ₹{r[1]} | Category: {r[2]} | Desc: {r[3]} | Date: {r[4]}")
    print()


    return rows

def delete_account(user_id):
    print("\n WARNING: This will permanently delete your account and all expense records!")
    confirm = input("Type YES to confirm: ")

    if confirm.upper() != "YES":
        print("Account deletion cancelled.\n")
        return

    cursor.execute("DELETE FROM expenses WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    print("Your account and all related data have been deleted permanently.\n")
    return "DELETED"
def sort_expenses(user_id):
    while True:
        print("""
    Sort Options:
    1. Amount High → Low
    2. Amount Low → High
    3. Date Newest → Oldest
    4. Date Oldest → Newest
    5. Main Menu
    """)

        choice = input("Choose option: ")

        if choice == "1":
            query = """
                SELECT local_id, amount, category, description, date 
                FROM expenses 
                WHERE user_id=%s 
                ORDER BY amount DESC
            """
        elif choice == "2":
            query = """
                SELECT local_id, amount, category, description, date 
                FROM expenses 
                WHERE user_id=%s 
                ORDER BY amount ASC
            """
        elif choice == "3":
            query = """
                SELECT local_id, amount, category, description, date 
                FROM expenses 
                WHERE user_id=%s 
                ORDER BY date DESC
            """
        elif choice == "4":
            query = """
                SELECT local_id, amount, category, description, date 
                FROM expenses 
                WHERE user_id=%s 
                ORDER BY date ASC
            """
        elif choice =="5":
            print("Back to Main Menu\n")
            return
        else:
            print("Invalid choice.\n")
            

        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        if not rows:
            print("No expenses found.\n")
            return

        print("\nSorted Expenses:\n")
        for r in rows:
            print(f"ID: {r[0]} | Amount: ₹{r[1]} | Category: {r[2]} | Desc: {r[3]} | Date: {r[4]}")
        print()


def plot_category_spending(user_id):
    cursor.execute("""
        SELECT category, SUM(amount) 
        FROM expenses 
        WHERE user_id = %s 
        GROUP BY category
    """, (user_id,))
    
    rows = cursor.fetchall()

    if not rows:
        print("No expenses found for visualization.\n")
        return

    df = pd.DataFrame(rows, columns=["Category", "Total"])
    
    print("""
1.Pie chart
2.Bar Garph
""")
    choice = input("Enter your choice of visualization")
    if choice == "1":
        plt.figure(figsize=(6, 6))
        plt.pie(df["Total"], labels=df["Category"], autopct="%1.1f%%")
        plt.title("Category-wise Spending (Pie Chart)")
        plt.show()
    elif choice == "2":
        plt.figure(figsize=(8, 6))
        sns.barplot(x="Category", y="Total", data=df)
        plt.title("Category-wise Spending (Bar Chart)")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.show()
    else:
        print("wrong Choice")
        return

def menu(user_id):
    while True:
        print("""
1. Add Expense
2. View Expenses
3. Update Expense
4. Delete Expense
5. Get Report
6. Sort Expenses
7. Expenses Graph
8. Logout
9. Delete Account
""")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense(user_id)
        elif choice == "2":
            while True:
                print("""
1. view Expenses
2. View Expenses by Category
3. View Expenses by Description
4. Main Menu                    
""" )
                choice_view = input("Enter choice for view")
                if choice_view=="1":
                    view_expenses(user_id)
                elif choice_view=="2":
                    view_by_category(user_id)
                elif choice_view =="3":
                    view_expense_by_description(user_id)
                elif choice_view == "4":
                    print("Back to Main Menu")
                    break
                    
                else:
                    print("Invalid Option/Choice\n")
        elif choice == "3":
            update_expense(user_id)
        elif choice == "4":
            delete_expense(user_id)
        elif choice =="5":
            while True:
               print("""
1.CSV
2.Excel
3.Monthly Report
4.Main Menu
""")
               choice_report = input("Enter your choice: ")

               if choice_report=="1":
                   report_csv(user_id)
               elif choice_report=="2":
                   report_excel(user_id)
               elif choice_report == "3":
                    report_monthly(user_id)
               elif choice_report =="4":
                   print("Back to Main Menu\n")
                   break
               else:
                     print("invalid option\n")           

            
        elif choice == "6":
            sort_expenses(user_id)
        elif choice=="7":
            plot_category_spending(user_id)
        elif choice == "8":
         print("log out\n")
         break
        elif choice=="9":
            delete_account(user_id)
            break
        else:
            print("invalid option")

while True:
    print("""
1. Register
2. Login
3. Exit
""")
    option = input("Choose option: ")

    if option == "1":
        register()
    elif option == "2":
        user_id = login()
        if user_id:
            menu(user_id)
    elif option == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid input.\n")