import json
import os
from typing import Set, Dict, Optional
from id_manager import IDManager


class User:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        surname: str,
        email: str,
        projects: Optional[Set["Project"]] = None
    ):
        self.id: int = IDManager.get_new_user_id() if id is None else id
        self.name: str = name
        self.surname: str = surname
        self.email: str = email
        self.projects: Set["Project"] = projects or set()

    def add_project(self, project: "Project") -> None:
        self.projects.add(project)

    def to_dict(self) -> Dict[str, any]:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects]
        }

    def update_user(
            self,
            name: Optional[str] = None,
            surname: Optional[str] = None,
            email: Optional[str] = None) -> None:
        if name:
            self.name = name
        if surname:
            self.surname = surname
        if email:
            self.email = email

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id or (
            self.email == other.email and self.name == other.name
        )

    def __str__(self) -> str:
        return f"{self.id}. {self.name} {self.surname} - {self.email}"

    def __repr__(self) -> str:
        return self.__str__()


class Users:
    users: Set[User] = set()

    @classmethod
    def add_user(cls, user: User) -> None:
        cls.users.add(user)

    @classmethod
    def save_to_file(cls, filename: str = "data/users.json") -> None:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump([user.to_dict() for user in cls.users], file, indent=4)

    @classmethod
    def set_users(cls, users: Set[User]) -> None:
        cls.users = users

    @classmethod
    def remove_user(cls, user: User) -> None:
        cls.users.discard(user)
