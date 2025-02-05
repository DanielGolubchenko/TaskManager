import hashlib
from datetime import datetime

class Task:
    # Default non-modifiable variables
    priority_defaults = ("Low", "Medium", "High", "Urgent")
    status_defaults = ("Pending", "In progress", "Completed", "Canceled")

    # Default modifiable variable
    tags_defaults = ["💼Trabajo",
                     "📚Estudios",
                     "🏠Hogar",
                     "🤝Reunión",
                     "🎯Objetivo",
                     "📖Lectura",
                     "🛒Compras",
                     "💳Facturas"]

    def __init__(self,
                 title,#🚧(unir match-case + modificable)🚧
                 priority,#🚧(unir match-case y validacion input respecto defaults)🚧
                 status,#🚧(unir match-case y validacion input respecto defaults)🚧
                 description=None,#🚧(unir match-case + modificable)🚧
                 due_date=None,#Opcional: DD/MM/YY. Hora opcional(Hour/min) 🚧(unir match-case + modificable)🚧
                 created_at=None,#🚧(unir match-case)🚧
                 updated_at=None,#🚧(unir match-case)🚧
                 tags=None, # 🚧(unir match-case + opción para modificar directa y libremente)🚧
                 task_id=None):#🚧(unir match-case)🚧
        self.title = title
        self._priority = priority
        self._status = status

        self.description = description if description is not None else []
        self.due_date = due_date if due_date is not None else []

        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()

        self.tags = tags if tags is not None else [] 

        self.task_id = task_id if task_id is not None else self.generate_task_id()

    #Generates unique task_id at task creation.
    def generate_task_id(self):
        data = (self.title + str(self.created_at)).encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    @property
    def priority(self):
        return self._priority
    
    # user-modifiable priority 🚧🚧
    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def status(self):
        return self._status
    
    # user-modifiable status 🚧🚧
    @status.setter
    def status(self, value):
        self._status = value