from auth import register, login
from expenses import (
    add_expense, view_expenses, view_by_category, view_by_description,
    update_expense, delete_expense,view_by_category, delete_account
)
from report import report_csv, report_excel, report_monthly
from visualize import plot_category_spending

def menu(user_id):
    while True:
        print("""
1. Add Expense
2. View Expenses
3. Update Expense
4. Delete Expense
5. Reports
6. Sort Expenses
7. Graphs
8. Logout
9. Delete Account
""")
        choice = input("Choose option: ")

        if choice == "1":
            add_expense(user_id)

        elif choice == "2":
            print("""
1. All Expenses
2. By Category
3. By Description
4. Back
""")
            ch = input("Enter: ")

            if ch == "1": view_expenses(user_id)
            elif ch == "2": view_by_category(user_id)
            elif ch == "3": view_by_description(user_id)

        elif choice == "3":
            update_expense(user_id)

        elif choice == "4":
            delete_expense(user_id)

        elif choice == "5":
            print("""
1. CSV
2. Excel
3. Monthly Report
4. Back
""")
            r = input("Enter: ")
            if r == "1": report_csv(user_id)
            if r == "2": report_excel(user_id)
            if r == "3": report_monthly(user_id)

        elif choice == "6":
            view_by_category(user_id)

        elif choice == "7":
            plot_category_spending(user_id)

        elif choice == "8":
            print("Logged out.")
            break

        elif choice == "9":
            if delete_account(user_id) == "DELETED":
                break


while True:
    print("""
1. Register
2. Login
3. Exit
""")
    option = input("Choose: ")

    if option == "1":
        register()

    elif option == "2":
        user_id = login()
        if user_id:
            menu(user_id)

    elif option == "3":
        print("Goodbye!")
        break

