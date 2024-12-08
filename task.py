from typing import Optional, Dict, Any
from enums import Priority, Status
from id_manager import IDManager


class Task:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: str,
        priority: Priority | str,
        status: Status = Status.NOT_STARTED,
        _type: Optional[str] = None
    ):
        if isinstance(priority, str):
            self.priority: Priority = Priority(priority)
        elif isinstance(priority, Priority):
            self.priority: Priority = priority
        else:
            raise ValueError("Invalid priority value")

        if isinstance(status, str):
            self.status: Status = Status(status)
        elif isinstance(status, Status):
            self.status: Status = status
        else:
            raise ValueError("Invalid status value")

        self.id: int = IDManager.get_new_user_id() if id is None else id
        self.name: str = name
        self.description: str = description
        self._type: Optional[str] = _type

    def update_task(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority | str] = None,
        **kwargs: Any
    ) -> None:
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if priority is not None:
            if isinstance(priority, Priority):
                self.priority = priority
            elif isinstance(priority, str):
                self.priority = Priority(priority)
            else:
                raise ValueError("Invalid priority value")

    def change_status(self, status: Status | str) -> None:
        if isinstance(status, Status):
            self.status = status
        elif isinstance(status, str):
            self.status = Status(status)
        else:
            raise ValueError("Invalid status value")

    def to_dict(self) -> Dict[str, Any]:
        task_dict: Dict[str, Any] = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            '_type': self._type
        }
        priority_map = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
        task_dict['priority'] = priority_map.get(self.priority.value, 2)
        return task_dict


class DevTask(Task):
    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: str,
        priority: Priority | str,
        language: str,
        status: Status = Status.NOT_STARTED
    ):
        super().__init__(id, name, description, priority, status, 'DevTask')
        self.language: str = language

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data['language'] = self.language
        return data

    def __str__(self) -> str:
        return f'{self.id}. {self.name} - {self.description} - {self.priority} - {self.status} - {self.language}'

    def __repr__(self) -> str:
        return self.__str__()

    def update_task(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority | str] = None,
        language: Optional[str] = None
    ) -> None:
        super().update_task(name=name, description=description, priority=priority)
        if language is not None:
            self.language = language


class QATask(Task):
    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: str,
        priority: Priority | str,
        test_type: str,
        status: Status = Status.NOT_STARTED
    ):
        super().__init__(id, name, description, priority, status, 'QATask')
        self.test_type: str = test_type

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data['test_type'] = self.test_type
        return data

    def __str__(self) -> str:
        return f'{self.id}. {self.name} - {self.description} - {self.priority} - {self.status} - {self.test_type}'

    def __repr__(self) -> str:
        return self.__str__()

    def update_task(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority | str] = None,
        test_type: Optional[str] = None
    ) -> None:
        super().update_task(name=name, description=description, priority=priority)
        if test_type is not None:
            self.test_type = test_type


class DocTask(Task):
    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: str,
        priority: Priority | str,
        document: str,
        status: Status = Status.NOT_STARTED
    ):
        super().__init__(id, name, description, priority, status, 'DocTask')
        self.document: str = document

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data['document'] = self.document
        return data

    def __str__(self) -> str:
        return f'{self.id}. {self.name} - {self.description} - {self.priority} - {self.status} - {self.document}'

    def __repr__(self) -> str:
        return self.__str__()

    def update_task(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority | str] = None,
        document: Optional[str] = None
    ) -> None:
        super().update_task(name=name, description=description, priority=priority)
        if document is not None:
            self.document = document
