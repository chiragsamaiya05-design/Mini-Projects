

from tasks import add_task, view_tasks, mark_done, delete_task


def main():
    while True:
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")
            
        choice = input("Enter your choice: ")

        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye ")
            break
        else:
            print(" Invalid choice. Try again.")

