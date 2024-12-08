class IDManager:
    """
    A utility class to manage unique IDs for users, projects, and tasks.
    """
    last_user_id: int = 0
    last_project_id: int = 0
    last_task_id: int = 0

    @classmethod
    def get_new_user_id(cls) -> int:
        """
        Generate a new unique ID for a user.
        """
        cls.last_user_id += 1
        return cls.last_user_id

    @classmethod
    def get_new_project_id(cls) -> int:
        """
        Generate a new unique ID for a project.
        """
        cls.last_project_id += 1
        return cls.last_project_id

    @classmethod
    def get_new_task_id(cls) -> int:
        """
        Generate a new unique ID for a task.
        """
        cls.last_task_id += 1
        return cls.last_task_id

    @classmethod
    def validate_id(cls, id_name: str, new_id: int) -> None:
        """
        Validate and update the last ID for a given entity if the new ID is greater.
        """
        current_id: int = getattr(cls, id_name, 0)
        if new_id > current_id:
            setattr(cls, id_name, new_id)

    @classmethod
    def validate_last_user_id(cls, new_id: int) -> None:
        """
        Validate and update the last user ID.
        """
        cls.validate_id('last_user_id', new_id)

    @classmethod
    def validate_last_project_id(cls, new_id: int) -> None:
        """
        Validate and update the last project ID.
        """
        cls.validate_id('last_project_id', new_id)

    @classmethod
    def validate_last_task_id(cls, new_id: int) -> None:
        """
        Validate and update the last task ID.
        """
        cls.validate_id('last_task_id', new_id)
