

from tasks import add_task, view_tasks, mark_done, delete_task
from auth import login, register

def menu(user_id):
    while True:
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")
            
        choice = input("Enter your choice: ")

        
        if choice == "1":
            add_task(user_id)
        elif choice == "2":
            view_tasks(user_id)
        elif choice == "3":
            mark_done(user_id)
        elif choice == "4":
            delete_task(user_id)
        elif choice == "5":
            print("Goodbye ")
            break
        else:
            print(" Invalid choice. Try again.")

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