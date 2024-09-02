def information():
    print("----- To-Do List -----")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Mark Tasks as Done")
    print("4. Exit")
    print("----------------------")
    
def add_task(tasks):
    try:
        count = int(input("How many tasks you want to add: "))
        for i in range(count):
            task_to_add = input("Enter the task: ")
            tasks.append({"task": task_to_add, "done": False})
            print("Task added!")
        print(tasks)
        print()
    except ValueError:
        print("Enter a valid number in order to continue!")
        
def show_tasks(tasks):    
    print()
    if len(tasks) > 0:
        print("Tasks:")    
        for i, task in enumerate(tasks):
            status = "Done" if task["done"] else "Not Done"
            # print(f"{i + 1}. {task["task"]} - {status}")
            print(i + 1, ".", task.get("task"), status)
    else: 
        print("There isn't any tasks to do.")
    print()

def mark_task(tasks):
    task_index = int(input("Enter the task number to mark as done: "))
    if len(tasks) > 0:
        try:
            if tasks[task_index - 1]["done"]:
                print("Task is already marked as done!")
            elif task_index <= len(tasks) and task_index > 0:
                tasks[task_index - 1]["done"] = True
                print("Task marked as done!")
            else:
                print("Invalid task number")
        except IndexError:
            print("Enter a task number within the range of", len(tasks))
    else:
        print("There is no task to mark as done!")
    
    
def main():
    tasks = []
    while True:
        try:
            information()
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Enter a valid number within the range of: 1-4")
            
        if 0 < choice <= 4:
            if choice == 1:
                add_task(tasks)
            elif choice == 2:
                show_tasks(tasks)
            elif choice == 3:
                mark_task(tasks)
            elif choice == 4:
                return False
        else:
            print("Enter a number within the range of: 1-4!")
    
if __name__ == "__main__":
    main()