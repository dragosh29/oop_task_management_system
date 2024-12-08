import json
from typing import Set, List, Dict, Any
from enums import Priority, Status
from user import User
from project import Project
from task import DevTask, QATask, DocTask
from id_manager import IDManager


class CustomEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for serializing User, Project, and Task objects.
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (User, Project, DevTask, QATask, DocTask)):
            return obj.to_dict()
        if isinstance(obj, (Priority, Status)):
            return obj.value
        return super().default(obj)


def serialize_to_file(data: Any, filename: str) -> None:
    """
    Serialize data to a JSON file.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, cls=CustomEncoder, indent=4)


def deserialize_from_file(filename: str) -> Set[User]:
    """
    Deserialize data from a JSON file into User objects.
    """
    try:
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                if data and isinstance(data, list) and isinstance(data[0], dict):
                    return _deserialize_users(data)
                else:
                    return set()
            except json.JSONDecodeError:
                return set()
    except FileNotFoundError:
        return set()


def _deserialize_users(data: List[Dict[str, Any]]) -> Set[User]:
    """
    Deserialize a list of user dictionaries into a set of User objects.
    """
    users: Set[User] = set()
    for user_data in data:
        projects = {_deserialize_project(proj) for proj in user_data.get("projects", [])}
        user = User(
            user_data["id"],
            user_data["name"],
            user_data["surname"],
            user_data["email"],
            projects
        )
        IDManager.validate_last_user_id(user.id)
        users.add(user)
    return users


def _deserialize_project(data: Dict[str, Any]) -> Project:
    """
    Deserialize a project dictionary into a Project object.
    """
    tasks = {_deserialize_task(task) for task in data.get("tasks", [])}
    IDManager.validate_last_project_id(data.get("id", 0))
    return Project(
        data.get("id"),
        data.get("name", "Untitled Project"),
        data.get("description", ""),
        tasks,
        data.get("deadline")
    )


def _deserialize_task(data: Dict[str, Any]) -> Any:
    """
    Deserialize a task dictionary into a specific Task object (DevTask, QATask, or DocTask).
    """
    task_type = data.pop('_type', None)
    priority_map = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
    data['priority'] = priority_map.get(data.get("priority", 2), "Medium")
    IDManager.validate_last_task_id(data.get("id", 0))

    if task_type == 'DevTask':
        return DevTask(**data)
    elif task_type == 'QATask':
        return QATask(**data)
    elif task_type == 'DocTask':
        return DocTask(**data)

    raise ValueError(f"Unknown task type: {task_type}")
