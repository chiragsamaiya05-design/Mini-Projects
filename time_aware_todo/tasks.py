from db import get_connect

conn = get_connect()
cursor = conn.cursor()

def add_task(user_id):
    name = input("Enter task name: ")
    duration = float(input("Enter task duration (in hours): "))

    cursor.execute("INSERT INTO tasks (user_id,name,duration) VALUES (%s,%s,%s) ", (user_id,name,duration,))
    conn.commit()
    print(" Task added!")
    cursor.close()
    conn.close()

def view_tasks(user_id):
    conn = get_connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks  WHERE user_id =%s",(user_id,))

    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    if not tasks:
                print(" No tasks found.")
    else:       
        print("\nTasks:")
        for t in tasks:
            status = "Done" if t["completed"] else "Not Done"
            print(f"{t['id']}.  {t['name']} | {t['duration']} hrs |[{status}]")
 
    
    return tasks

def mark_done(user_id):
   
    task_id = int(input("Enter task ID: "))
    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s  AND user_id= %s", (task_id,user_id))
    conn.commit()

    print(" Task marked as done!")
    cursor.close()
    conn.close()
    view_tasks(user_id)

def delete_task(user_id):
    conn = get_connect()
    cursor = conn.cursor()
    
    task_id = int(input("Enter task ID: "))
   
    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id =%s" , (task_id,user_id))
    conn.commit()
    print(" Task deleted!")
    cursor.close()
    conn.close()
    view_tasks(user_id)