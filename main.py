import sequencer
from user import User, Users
from project import Project
from task import DevTask, QATask, DocTask
import atexit
from enums import Priority, Status


def filter_tasks_by_status(status: str):
    tasks = {}
    status = Status[status]
    for user in Users.users:
        for project in user.projects:
            key = f"{user.name} - {project.name}"
            tasks[key] = [task for task in project.tasks if task.status == status]
            tasks[key].sort(key=lambda x: x.priority.value)
            if not tasks[key]:
                del tasks[key]
    return tasks


def filter_tasks_by_priority(priority: str):
    tasks = {}
    priority = Priority[priority]
    for user in Users.users:
        for project in user.projects:
            key = f"{user.name} - {project.name}"
            tasks[key] = [task for task in project.tasks if task.priority == priority]
            tasks[key].sort(key=lambda x: x.priority.value)
            if not tasks[key]:
                del tasks[key]
    return tasks


def filter_tasks():
    tasks = {}
    while True:
        print("\nFilter Tasks:")
        print("1. By Status")
        print("2. By Priority")
        print("3. Back to Main Menu")
        choice = input("Select an option: ")
        if choice == "1":
            status = input("Enter status (Not Started, In Progress, Completed): ")
            if status not in ["Not Started", "In Progress", "Completed"]:
                print("Invalid status. Please try again.")
                continue
            status = status.replace(" ", "_").upper()
            tasks = filter_tasks_by_status(status)
        elif choice == "2":
            priority = input("Enter priority (Low, Medium, High, Critical): ")
            if priority not in ["Low", "Medium", "High", "Critical"]:
                print("Invalid priority. Please try again.")
                continue
            tasks = filter_tasks_by_priority(priority.upper())
        elif choice == "3":
            break
        else:
            print("Invalid option. Please try again.")

        print("\nFiltered Tasks:")

        if not tasks.items():
            print("No tasks found matching the criteria.")

        for key, value in tasks.items():
            print(f"{key}:")
            for task in value:
                print(f"\t{task}")


def change_task_status():
    user_id = int(input("Enter User ID for the task: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    project_id = int(input("Enter Project ID for the task: "))
    project = next((p for p in user.projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    task_id = int(input("Enter Task ID to change status: "))
    task = next((t for t in project.tasks if t.id == task_id), None)
    if not task:
        print("Task not found.")
        return

    while True:
        new_status = input("Enter new status (Not Started, In Progress, Completed): ")
        if new_status not in ["Not Started", "In Progress", "Completed"]:
            print("Invalid status. Please try again.")
        else:
            task.change_status(new_status)
            break

    print(f"Task {task_id} status changed successfully.")


def save_data():
    Users.save_to_file()


def display_state():
    print("\nCurrent State of Task Management System:")
    if not Users.users:
        print("Task management system is empty.")
        return

    print("Users:")
    for user in Users.users:
        print(user)
        print("\tProjects:")
        for project in user.projects:
            print(f"\t{project}")
            print("\t\tTasks:")
            for task in project.tasks:
                print(f"\t\t{task}")


def create_user():
    name = input("Enter User Name: ")
    surname = input("Enter User Surname: ")
    email = input("Enter User Email: ")
    user = User(None, name, surname, email)
    Users.add_user(user)
    print(f"User {name} created successfully.")


def update_user():
    user_id = int(input("Enter User ID to update: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    name = input(f"Enter new name (current: {user.name}): ") or user.name
    surname = input(f"Enter new surname (current: {user.surname}): ") or user.surname
    email = input(f"Enter new email (current: {user.email}): ") or user.email

    user.update_user(name, surname, email)
    print(f"User {user_id} updated successfully.")


def remove_user():
    user_id = int(input("Enter User ID to remove: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    Users.users.remove(user)
    print(f"User {user_id} removed successfully.")


def create_project():
    user_id = int(input("Enter User ID for the project: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    name = input("Enter Project Name: ")
    description = input("Enter Project Description: ")
    deadline = input("Enter Project Deadline (YYYY-MM-DD): ")

    project = Project(None, name, description, [], deadline)
    user.add_project(project)
    print(f"Project {name} created and assigned to user {user.name}.")


def update_project():
    user_id = int(input("Enter User ID for the project: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    project_id = int(input("Enter Project ID to update: "))
    project = next((p for p in user.projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    name = input(f"Enter new project name (current: {project.name}): ") or project.name
    description = input(f"Enter new description (current: {project.description}): ") or project.description
    deadline = input(f"Enter new deadline (current: {project.deadline}): ") or project.deadline

    project.update_project(name, description, deadline)
    print(f"Project {project_id} updated successfully.")


def remove_project():
    user_id = int(input("Enter User ID for the project: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    project_id = int(input("Enter Project ID to remove: "))
    project = next((p for p in user.projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    user.projects.remove(project)
    print(f"Project {project_id} removed successfully.")


def create_task():
    user_id = int(input("Enter User ID for the task: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    project_id = int(input("Enter Project ID for the task: "))
    project = next((p for p in user.projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    task_type = input("Enter Task Type (DevTask, QATask, DocTask): ")
    name = input("Enter Task Name: ")
    description = input("Enter Task Description: ")
    priority = input("Enter Task Priority (Low, Medium, High, Critical): ")
    while priority not in ["Low", "Medium", "High", "Critical"]:
        print("Invalid priority. Please try again.")
        priority = input("Enter Task Priority (Low, Medium, High, Critical): ")

    if task_type == "DevTask":
        language = input("Enter Programming Language: ")
        task = DevTask(None, name, description, priority, language)
    elif task_type == "QATask":
        test_type = input("Enter Test Type: ")
        task = QATask(None, name, description, priority, test_type)
    elif task_type == "DocTask":
        document = input("Enter Document Type: ")
        task = DocTask(None, name, description, priority, document)
    else:
        print("Invalid task type.")
        return

    project.add_task(task)
    print(f"{task_type} {name} created and assigned to project {project.name}.")


def update_task():
    user_id = int(input("Enter User ID for the task: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    project_id = int(input("Enter Project ID for the task: "))
    project = next((p for p in user.projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    task_id = int(input("Enter Task ID to update: "))
    task = next((t for t in project.tasks if t.id == task_id), None)
    if not task:
        print("Task not found.")
        return

    name = input(f"Enter new task name (current: {task.name}): ") or task.name
    description = input(f"Enter new description (current: {task.description}): ") or task.description
    priority = input(f"Enter new priority (current: {task.priority}): ") or task.priority

    task.update_task(name=name, description=description, priority=priority)
    print(f"Task {task_id} updated successfully.")


def remove_task():
    user_id = int(input("Enter User ID for the task: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    project_id = int(input("Enter Project ID for the task: "))
    project = next((p for p in user.projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    task_id = int(input("Enter Task ID to remove: "))
    task = next((t for t in project.tasks if t.id == task_id), None)
    if not task:
        print("Task not found.")
        return

    project.tasks.remove(task)
    print(f"Task {task_id} removed successfully.")


def list_users():
    print("\nUsers:")
    for user in Users.users:
        print(user)


def list_projects():
    user_id = int(input("Enter User ID to list projects: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    print(f"\nProjects for User {user.name}:")
    for project in user.projects:
        print(project)


def list_tasks():
    user_id = int(input("Enter User ID for the task: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    project_id = int(input("Enter Project ID for the task: "))
    project = next((p for p in user.projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    print(f"\nTasks for Project {project.name}:")
    for task in project.tasks:
        print(task)


def load_data():
    users = None
    try:
        users = sequencer.deserialize_from_file('data/users.json')
    except Exception as e:
        print(f"Error loading data: {e}")
    if users:
        Users.users = users
    else:
        print("No data loaded.")


def main_menu():
    menu = {
        "1": ("Users", {
            "1": ("Create User", create_user),
            "2": ("List Users", list_users),
            "3": ("Update User", update_user),
            "4": ("Remove User", remove_user),
            "5": ("Back to Main Menu", None)
        }),
        "2": ("Projects", {
            "1": ("Create Project", create_project),
            "2": ("List Projects", list_projects),
            "3": ("Update Project", update_project),
            "4": ("Remove Project", remove_project),
            "5": ("Back to Main Menu", None)
        }),
        "3": ("Tasks", {
            "1": ("Create Task", create_task),
            "2": ("List Tasks", list_tasks),
            "3": ("Update Task", update_task),
            "4": ("Remove Task", remove_task),
            "5": ("Change Task Status", change_task_status),
            "6": ("Filter Tasks", filter_tasks),
            "7": ("Back to Main Menu", None)
        }),
        "4": ("Display State", display_state),
        "5": ("Exit", exit)
    }

    # Load data on start-up
    load_data()

    # Ensure data is saved on program exit
    atexit.register(save_data)

    while True:
        print("\nMain Menu:")
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")

        choice = input("Select an option: ")
        if choice not in menu:
            print("Invalid option. Please try again.")
            continue

        description, sub_menu_or_function = menu[choice]
        if isinstance(sub_menu_or_function, dict):
            while True:
                print(f"\n{description} Menu:")
                for sub_key, (sub_desc, _) in sub_menu_or_function.items():
                    print(f"{sub_key}. {sub_desc}")

                sub_choice = input("Select an option: ")
                if sub_choice not in sub_menu_or_function:
                    print("Invalid option. Please try again.")
                    continue

                sub_desc, sub_function = sub_menu_or_function[sub_choice]
                if sub_function is None:
                    break  # Go back to the main menu
                sub_function()
        else:
            sub_menu_or_function()


if __name__ == "__main__":
    main_menu()
