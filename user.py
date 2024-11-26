import json
from project import Project

class User:
    def __init__(self, id, name, surname, email, projects=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.projects = set(projects) if projects else set()

    def add_project(self, project):
        self.projects.add(project)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects]
        }

    @classmethod
    def from_dict(cls, data):
        projects = {Project.from_dict(proj) for proj in data.get("projects", [])}
        return cls(data["id"], data["name"], data["surname"], data["email"], projects)

class Users:
    users = set()

    @classmethod
    def add_user(cls, user):
        cls.users.add(user)

    @classmethod
    def save_to_file(cls, filename="data/users.json"):
        with open(filename, 'w') as file:
            json.dump([user.to_dict() for user in cls.users], file, indent=4)

    @classmethod
    def load_from_file(cls, filename="data/users.json"):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                cls.users = {User.from_dict(user_data) for user_data in data}
        except FileNotFoundError:
            cls.users = set()
