from enums import Priority, Status

class Task:
    def __init__(self, id, name, description, priority, status=Status.NOT_STARTED, _type=None):
        if isinstance(priority, str):
            self.priority = Priority(priority.upper())
        elif isinstance(priority, Priority):
            self.priority = priority
        else:
            raise ValueError("Invalid priority value")

        if isinstance(status, str):
            self.status = Status(status.replace(" ", "_").upper())
        elif isinstance(status, Status):
            self.status = status
        else:
            raise ValueError("Invalid status value")

        self.id = id
        self.name = name
        self.description = description
        self._type = _type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            '_type': self._type
        }

class DevTask(Task):
    def __init__(self, id, name, description, priority, language, status=Status.NOT_STARTED):
        super().__init__(id, name, description, priority, status, 'DevTask')
        self.language = language

    def to_dict(self):
        data = super().to_dict()
        data['language'] = self.language
        return data

class QATask(Task):
    def __init__(self, id, name, description, priority, test_type, status=Status.NOT_STARTED):
        super().__init__(id, name, description, priority, status, 'QATask')
        self.test_type = test_type

    def to_dict(self):
        data = super().to_dict()
        data['test_type'] = self.test_type
        return data

class DocTask(Task):
    def __init__(self, id, name, description, priority, document, status=Status.NOT_STARTED):
        super().__init__(id, name, description, priority, status, 'DocTask')
        self.document = document

    def to_dict(self):
        data = super().to_dict()
        data['document'] = self.document
        return data
