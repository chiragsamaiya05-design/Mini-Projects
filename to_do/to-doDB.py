import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="ChiragSamaiya",       
    database="todo_app"
)

cursor = db.cursor()


def show_menu():
    print("1. Add a Task" )
    print("2. View Task")
    print("3. Delete a Task" )
    print("4. Mark a task as completed/n" )
    print("5. Exit")

def add_task():
    a = input("Enter your tasks:")
    sql = "INSERT INTO tasks(task) VALUES (%s)"
    cursor.execute(sql,(a,))
    db.commit()

    print("Task added")

    

   


def view_task():
     cursor.execute("SELECT id, task, completed FROM tasks")
     rows = cursor.fetchall()


     for r in rows:
         id,task,completed = r
         status = "Done"if completed else "Not Done"
         print(f"{id},{task}[{status}]")
       

def delete_task():
    view_task()
    id = int(input("enter task Id to delete"))

    

    cursor.execute("DELETE FROM tasks WHERE id =%s",(id,))
    db.commit()

    print("Task is Deleted !")



def mark_down():
    view_task()

    id = int(input("Enter task ID to mark as completed: "))

    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id =%s",(id,))
    db.commit()
    

    print("Task marked completed")

def main():
    while True:
        show_menu()

        choice = int(input("Enter your choice:"))

        if(choice== 1):
            add_task()
        elif(choice == 2):
           view_task()
        elif(choice==3):
          delete_task()
        elif(choice == 4):
           mark_down()
        elif(choice == 5):
           print("Thankyou for using To-Do")
           break
        else:
            print("wrong choice!")

main()
