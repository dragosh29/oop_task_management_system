from typing import Set
from task import DevTask, QATask, DocTask
from datetime import datetime, timedelta

import json


class Project:
    def __init__(self, id, name, description, tasks=None, deadline=None):
        self.id = id
        self.name = name
        self.description = description
        self.tasks = set()

        # all the tasks belonging to the project
        if tasks is not None:
            """
            might be the case when the project is loaded from the disk, the tasks are not 
            yet deserialized, but it is a dictionary
            """
            for task in tasks:
                task_type = task.pop('_type', None)
                if isinstance(task, dict) and task_type == 'DevTask':
                    task = DevTask(**task)
                elif isinstance(task, dict) and task_type == 'QATask':
                    task = QATask(**task)
                elif isinstance(task, dict) and task_type == 'DocTask':
                    task = DocTask(**task)
                else:
                    raise ValueError(f'Unknown task type: {task}')
                self.tasks.add(task)
        else:
            self.tasks = set()

        # when the project should be completed
        if deadline is not None:
            self.deadline = (
                datetime.fromisoformat(deadline) if isinstance(deadline, str) else deadline
            )
        else:
            # by default add a date 30 days from now
            self.deadline = (
                datetime.fromisoformat(deadline) if isinstance(deadline, str) else deadline
            )

    def __eq__(self, other):
        if not isinstance(other, Project):
            return False
        return self.name == other.name and self.description == other.description

    def __hash__(self):
        return hash((self.name, self.description))

    def add_task(self, task):
        self.tasks.add(task)

    def __str__(self):
        return f'{self.name} - {self.description}'

    def __repr__(self):
        return f'{self.name} - {self.description}'

    def set_deadline(self, deadline):
        self.deadline = deadline

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tasks': [task.to_dict() for task in self.tasks],
            'deadline': self.deadline.strftime('%Y-%m-%d') if isinstance(self.deadline, datetime) else self.deadline
        }

    def describe(self):
        return f'{self.name} - {self.description} - {self.deadline} - {self.tasks}'


class ProjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Project):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Projects:
    """
    Class to manage projects
    """

    # all the classes see the same set of projects
    projects = set()

    @classmethod
    def add_project(cls, project: Project) -> None:
        cls.projects.add(project)

    @classmethod
    def remove_project(cls, project: Project) -> None:
        cls.projects.remove(project)

    @classmethod
    def get_projects(cls) -> Set[Project]:
        return cls.projects