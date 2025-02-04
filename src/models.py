import hashlib
from datetime import datetime

class Task:
    def __init__(self,
                 title,
                 priority,
                 status,
                 description=None,
                 due_date=None,
                 created_at=None,
                 updated_at=None,
                 tags=None,
                 assigned_to=None,
                 completed=False,
                 task_id=None):
        self.title = title
        self.priority = priority
        self.status = status

        self.description = description if description is not None else []
        self.due_date = due_date if due_date is not None else []

        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()

        self.tags = tags if tags is not None else []

        self.assigned_to = assigned_to
        self.completed = completed

        self.task_id = task_id if task_id is not None else self.generate_task_id()

    def generate_task_id(self):
        data = (self.title + str(self.created_at)).encode('utf-8')
        return hashlib.sha256(data).hexdigest()