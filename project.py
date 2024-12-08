import os
from typing import Set, Optional, Dict, Any
from datetime import datetime, timedelta
from id_manager import IDManager
import json


class Project:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: str,
        tasks: Optional[Set["Task"]] = None,
        deadline: Optional[str | datetime] = None
    ):
        self.id: int = IDManager.get_new_project_id() if id is None else id
        self.name: str = name
        self.description: str = description
        self.tasks: Set["Task"] = tasks or set()

        # Handle deadline
        self.deadline: Optional[datetime] = self._parse_deadline(deadline)

    @staticmethod
    def _parse_deadline(deadline: Optional[str | datetime]) -> Optional[datetime]:
        if isinstance(deadline, str) and deadline.strip():
            return datetime.fromisoformat(deadline)
        elif isinstance(deadline, datetime):
            return deadline
        else:
            return datetime.now() + timedelta(days=30)  # Default to 30 days from now

    def add_task(self, task: "Task") -> None:
        self.tasks.add(task)

    def remove_task(self, task: "Task") -> None:
        self.tasks.discard(task)

    def set_deadline(self, deadline: str | datetime) -> None:
        self.deadline = self._parse_deadline(deadline)

    def update_project(self, name: Optional[str] = None, description: Optional[str] = None, deadline: Optional[str | datetime] = None) -> None:
        if name:
            self.name = name
        if description:
            self.description = description
        if deadline:
            self.set_deadline(deadline)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tasks": [task.to_dict() for task in self.tasks],
            "deadline": self.deadline.strftime('%Y-%m-%d') if self.deadline else None
        }

    def describe(self) -> str:
        return f"{self.id}. {self.name} - {self.description} - {self.deadline} - {len(self.tasks)} tasks"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Project):
            return False
        return self.name == other.name and self.description == other.description

    def __hash__(self) -> int:
        return hash((self.name, self.description))

    def __str__(self) -> str:
        return f"{self.id}. {self.name} - {self.description}"

    def __repr__(self) -> str:
        return self.__str__()


class ProjectEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Project):
            return obj.to_dict()
        return super().default(obj)


class Projects:
    """
    Class to manage projects
    """
    projects: Set[Project] = set()

    @classmethod
    def add_project(cls, project: Project) -> None:
        cls.projects.add(project)

    @classmethod
    def remove_project(cls, project: Project) -> None:
        cls.projects.discard(project)  # use discard to avoid KeyError if project does not exist

    @classmethod
    def get_projects(cls) -> Set[Project]:
        return cls.projects

    @classmethod
    def save_to_file(cls, filename: str = "data/projects.json") -> None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump([project.to_dict() for project in cls.projects], file, cls=ProjectEncoder, indent=4)

    @classmethod
    def load_from_file(cls, filename: str = "data/projects.json") -> None:
        if not os.path.exists(filename):
            print(f"File not found: {filename}. No projects loaded.")
            return

        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                cls.projects = {Project(**proj) for proj in data}
            except json.JSONDecodeError:
                print(f"Invalid JSON in file: {filename}. No projects loaded.")
