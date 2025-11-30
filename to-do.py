task =[]
file_name = "file.txt"


def load_file():
    with open("file.txt","r") as f:
        for line in f:
                tsk, status = line.strip().split(" | ")
                task.append({"task": tsk, "completed": status == "True"})

def save_task():
    with open("file.txt", "w") as f:
        for t in task:
            task_name = t.get("task", "")
            completed = t.get("completed", False)
            f.write(f"{task_name} | {completed}\n")

def show_menu():
    print("1. Add a Task" )
    print("2. View Task")
    print("3. Delete a Task" )
    print("4. Mark a task as completed/n" )
    print("5. Exit")

def add_task():
    a = input("Enter your tasks:")
    task.append({"task" : a,"completed ": False})
    save_task()
    print("Task is saved")


def view_task():
    for i,t in enumerate(task, start=1): 
        status = "Done" if t.get("completed",False) else " not done"
        print(f"{i}.{t['task']}[{status}]")
       

def delete_task():
    view_task()
    if(not task):

        print("No task your entered today:")
        return
    i = int(input("Which task you want to delete:"))
    task.pop(i -1 )
    save_task()
    print("Task is Deleted")
    ##for tas in task:
      ##  task.remove(i)   

def mark_down():
    view_task()
    if( not task):
        return
    num = int(input(" Enter Task to mark as completed"))
    task[num - 1]["completed"]= True
    save_task()
    print("Task is marked as completed")
    

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