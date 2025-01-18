import hashlib

class Task:
    def __init__(self,
                 title,
                 description,
                 due_date,
                 priority,
                 status,
                 created_at,
                 updated_at,
                 tags,
                 assigned_to=None,
                 completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.tags = tags
        self.assigned_to = assigned_to
        self.completed = completed

        self.task_id = self.generate_task_id()

    def generate_task_id(self):
        data = (self.title + str(self.created_at)).encode('utf-8')
        task_id = hashlib.sha256(data).hexdigest()
        return task_id