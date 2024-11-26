import json
from enums import Priority, Status
from user import User
from project import Project
from task import DevTask, QATask, DocTask

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (User, Project, DevTask, QATask, DocTask)):
            return obj.to_dict()
        if isinstance(obj, Priority):
            return obj.value
        if isinstance(obj, Status):
            return obj.value
        return super().default(obj)

def serialize_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, cls=CustomEncoder, indent=4)

def deserialize_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return _deserialize_users(data)
    except FileNotFoundError:
        return set()

def _deserialize_users(data):
    users = set()
    for user_data in data:
        projects = {_deserialize_project(proj) for proj in user_data.get("projects", [])}
        user = User(user_data["id"], user_data["name"], user_data["surname"], user_data["email"], projects)
        users.add(user)
    return users

def _deserialize_project(data):
    tasks = {_deserialize_task(task) for task in data.get("tasks", [])}
    return Project(data["id"], data["name"], data["description"], tasks, data.get("deadline"))

def _deserialize_task(data):
    task_type = data.pop('_type', None)
    if task_type == 'DevTask':
        return DevTask(**data)
    elif task_type == 'QATask':
        return QATask(**data)
    elif task_type == 'DocTask':
        return DocTask(**data)
    raise ValueError(f"Unknown task type: {task_type}")
