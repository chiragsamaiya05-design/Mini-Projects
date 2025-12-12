import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="ChiragSamaiya",       
    database="todo_app"
)

cursor = db.cursor()


def register_user():
    username = input("Enter usename :")
    password = input("Enter password :")

    cursor.execute("INSERT INTO users(username,password)VALUES(%s,%s)")
    db.commit()
    print("Registration successful!\n")


def login_user():
      username = input("Username: ")
      password = input("Password: ")

      cursor.execute("SELECT id FROM users WHERE username = %s  AND password = %s",(username,password))
    
      result = cursor.fetchone()

      if result:
          print("Login Successfully")
          return result[0]
      else:
          print("Invalid username or Password")
          return None


def show_main_menu():
    print("""
==== MAIN MENU ====
1. Register
2. Login
3. Exit
""")
def show_admin_menu():
    print("""
==== ADMIN MENU ====
1. View All Users
2. View All Tasks
3. Delete User
4. Delete Task
5. Logout
""")

def show_menu():
    print("1. Add a Task" )
    print("2. View Task")
    print("3. Delete a Task" )
    print("4. Mark a task as completed/n" )
    print("5. Logout")

def add_task(user_id):
    a = input("Enter your tasks:")
    sql = "INSERT INTO tasks(user_id,task) VALUES (%s,%s)"
    cursor.execute(sql,(user_id,a))
    db.commit()

    print("Task added")

    

   


def view_task(user_id):
     cursor.execute("SELECT id, task, completed FROM tasks")
     rows = cursor.fetchall()


     for r in rows:
         id,task,completed = r
         status = "Done"if completed else "Not Done"
         print(f"{id},{task}[{status}]")
       

def delete_task(user_id):
    view_task(user_id)
    id = int(input("enter task Id to delete"))

    

    cursor.execute("DELETE FROM tasks WHERE id =%s",(id,user_id))
    db.commit()

    print("Task is Deleted !")



def mark_down(user_id):
    view_task(user_id)

    id = int(input("Enter task ID to mark as completed: "))

    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id =%s",(id,user_id))

    db.commit()
    

    print("Task marked completed")


def admin_view():
    cursor.execute("SELECT id,user_name,rol FROM users")
    cursor.fetchall()

    print("\n===All Users===\n")
    for uid , uname, role in rows:
        print(f"{uid}| Username : {uname}|  Role :{role}")
    print()


def admin_view_task():
    cursor.execute("""
        SELECT tasks.id, users.username, tasks.task, tasks.completed
        FROM tasks
        JOIN users ON tasks.user_id = users.id
    """)

    rows = cursor.fetchall()

    print("\n===All Task===\n")
    for id,uname,task,comp in rows:
        status ="done"if comp else "Not Done"
        print(f"{id}.{task} by {uname}[{status}]")
    print()

def admin_delete_user():
    admin_view()
    uid = input("Enter user ID to delete: ")

    cursor.execute("DELETE FROM tasks WHERE user_id=%s", (uid,))
    cursor.execute("DELETE FROM users WHERE id=%s", (uid,))
    db.commit()
    print("User deleted!\n")


def admin_delete_task():
    admin_view_task()
    tid = input("Enter task ID to delete: ")

    cursor.execute("DELETE FROM tasks WHERE id=%s", (tid,))
    db.commit()
    print("Task deleted!\n")



def main():
    while True:
        show_main_menu()
        choice = input("Choose (1-3): ")

        if choice == "1":
            register_user()

        elif choice == "2":
            user_id, role = login_user()
            if user_id:

                # USER PANEL
                if role == "user":
                    while True:
                        show_user_menu()
                        ch = input("Choose (1-5): ")

                        if ch == "1": add_task(user_id)
                        elif ch == "2": view_tasks(user_id)
                        elif ch == "3": delete_task(user_id)
                        elif ch == "4": mark_complete(user_id)
                        elif ch == "5": break
                        else: print("Invalid option!\n")

                # ADMIN PANEL
                elif role == "admin":
                    while True:
                        show_admin_menu()
                        ch = input("Choose (1-5): ")

                        if ch == "1": admin_view()
                        elif ch == "2": admin_view_task()
                        elif ch == "3": admin_delete_user()
                        elif ch == "4": admin_delete_task()
                        elif ch == "5": break
                        else: print("Invalid option!\n")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!\n")



main()
