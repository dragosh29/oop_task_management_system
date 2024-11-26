from user import User, Users
from project import Project
from task import DevTask, QATask, DocTask
import atexit

def create_user():
    id = int(input("Enter User ID: "))
    name = input("Enter User Name: ")
    surname = input("Enter User Surname: ")
    email = input("Enter User Email: ")
    user = User(id, name, surname, email)
    Users.add_user(user)
    print(f"User {name} created successfully.")

def list_users():
    if not Users.users:
        print("No users available.")
        return
    for user in Users.users:
        print(user)

def create_project():
    user_id = int(input("Enter User ID for the project: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    id = int(input("Enter Project ID: "))
    name = input("Enter Project Name: ")
    description = input("Enter Project Description: ")
    deadline = input("Enter Project Deadline (YYYY-MM-DD): ")

    project = Project(id, name, description, [], deadline)
    user.add_project(project)
    print(f"Project {name} created and assigned to user {user.name}.")

def list_projects():
    user_id = int(input("Enter User ID to list projects: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    if not user.projects:
        print("No projects available for this user.")
        return

    for project in user.projects:
        print(project)

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
    id = int(input("Enter Task ID: "))
    name = input("Enter Task Name: ")
    description = input("Enter Task Description: ")
    priority = input("Enter Task Priority (Low, Medium, High, Critical): ")

    if task_type == "DevTask":
        language = input("Enter Programming Language: ")
        task = DevTask(id, name, description, priority, language)
    elif task_type == "QATask":
        test_type = input("Enter Test Type: ")
        task = QATask(id, name, description, priority, test_type)
    elif task_type == "DocTask":
        document = input("Enter Document Type: ")
        task = DocTask(id, name, description, priority, document)
    else:
        print("Invalid task type.")
        return

    project.add_task(task)
    print(f"{task_type} {name} created and assigned to project {project.name}.")

def list_tasks():
    user_id = int(input("Enter User ID to list tasks: "))
    user = next((u for u in Users.users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return

    project_id = int(input("Enter Project ID to list tasks: "))
    project = next((p for p in user.projects if p.id == project_id), None)
    if not project:
        print("Project not found.")
        return

    if not project.tasks:
        print("No tasks available for this project.")
        return

    for task in project.tasks:
        print(task)

def save_data():
    Users.save_to_file()
    print("Data saved successfully.")

def load_data():
    Users.load_from_file()
    print("Data loaded successfully.")

def main_menu():
    menu = {
        "1": ("Users", {
            "1": ("Create User", create_user),
            "2": ("List Users", list_users),
            "3": ("Back to Main Menu", None)
        }),
        "2": ("Projects", {
            "1": ("Create Project", create_project),
            "2": ("List Projects", list_projects),
            "3": ("Back to Main Menu", None)
        }),
        "3": ("Tasks", {
            "1": ("Create Task", create_task),
            "2": ("List Tasks", list_tasks),
            "3": ("Back to Main Menu", None)
        }),
        "4": ("Save Data", save_data),
        "5": ("Load Data", load_data),
        "6": ("Exit", exit)
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
