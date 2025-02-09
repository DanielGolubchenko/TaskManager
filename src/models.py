import hashlib
from datetime import datetime

class Task:
    # Default non-modifiable variables
    priority_defaults = ("Low", "Medium", "High", "Urgent")
    status_defaults = ("Pending", "In progress", "Completed", "Canceled")

    # Default modifiable variable
    tags_defaults = ["Work",
                     "Studies",
                     "Home",
                     "Meetings",
                     "Goals",
                     "Reading",
                     "Shopping",
                     "Bills"]

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

    # Generates unique task_id at task creation.
    def generate_task_id(self):
        data = (self.title + str(self.created_at)).encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    @property
    def priority(self):
        return self._priority
    
    # User-modifiable priority 🚧🚧
    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def status(self):
        return self._status
    
    # User-modifiable status 🚧🚧
    @status.setter
    def status(self, value):
        self._status = value

class TaskManager:

    def __init__(self, name="task_manager", ):
        self.name = name
        # Cumulative task variable
        self.tasks_list = []

    def add_task(self):
        print("Those entries with the symbol (*) are mandatory.")

        title = TaskManager.validation("title")
        priority = TaskManager.validation("priority")
        status = TaskManager.validation("status")
        description = TaskManager.validation("description")
        due_date = TaskManager.validation("due_date")
        tags = TaskManager.validation("tags")

        task = Task(title, priority, status, description, due_date, tags)
        self.tasks_list.append(task)
        print("Task added succesfully!")

    def show_tasks(self):
        pass

    def find_task(self):
        pass
    
    def modify_task(self):
        pass

    def delete_task(self):
        pass

    # Validates each posible task atribute input
    @staticmethod
    def validation(value):
        match value:
            case "title":
                while True:
                    print()
                    try:
                        user_input = input("Title(*): ").strip()
                        if user_input: return user_input
                        else: raise EmptyError
                    except EmptyError: print("This slot can't be empty.")

            case "priority":
                while True:
                    print()
                    # Display available options for priority selection
                    print(f"Options -> {Task.priority_defaults}", end=", ")
                    try:
                        # Prompt the user for a priority and validate input
                        user_input = input("Priority(*): ").strip()
                        if not user_input: raise EmptyError
                        elif user_input.lower() not in ["low", "medium", "high", "urgent"]:
                            raise NotAnOptionError
                        else: return user_input.capitalize()
                    except EmptyError: print("This slot can't be empty.")
                    except NotAnOptionError: print("That's not a valid option.")

            case "status":
                while True:
                    print()
                    # Display available options for status selection
                    print(f"Options -> {Task.status_defaults}", end=", ")
                    try:
                        # Prompt the user for a status and validate input
                        user_input = input("Status(*): ").strip()
                        if not user_input: raise EmptyError
                        elif user_input.lower() not in ["pending", "in progress", "completed", "canceled"]:
                            raise NotAnOptionError
                        else: return user_input.capitalize()
                    except EmptyError: print("This slot can't be empty.")
                    except NotAnOptionError: print("That's not a valid option.")

            case "description":
                print()
                # Get the task description (optional). If empty, return None.
                user_input = input("Description (press 'Enter' to skip): ").strip()
                return user_input if user_input else None

            case "due_date":
                while True:
                    print()
                    # Prompt user for a due date (can be just a date or date with time)
                    user_input = input("Enter due date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM), or press 'Enter' to skip: ").strip()
                    if not user_input:
                        return None # If input is empty, skip due date
                    try:
                        if " " in user_input:
                            # If input contains a space, assume it includes time (DD-MM-YYYY HH:MM)
                            due_date = datetime.strptime(user_input, "%d-%m-%Y %H:%M")
                        else:
                            # Otherwise, assume it's just a date (DD-MM-YYYY)
                            due_date = datetime.strptime(user_input, "%d-%m-%Y").date()
                        # Return date or datetime object based on input 
                        return due_date
                    except ValueError:
                        # Handle invalid date format (e.g., wrong separator, missing digits, invalid date)
                        print("Invalid format. Use 'DD-MM-YYYY' or 'DD-MM-YYYY HH:MM'.")

            case "tags":
                # Initialize an empty list to store the selected tags
                selected_tags = []

                while True:
                    # Presenting the available options for tag management
                    print()
                    print(f"Options -> {Task.tags_defaults}", end=", ")
                    print("1. Choose a default tag")
                    print("2. Modify a default tag")
                    print("3. Create a new tag")
                    print("4. Skip (no tags)")
                   
                    # Ensure the user input is one of the valid options (1-4)
                    try:
                        choice = input("\nEnter the number (1-4) for your choice: ").strip()
                        if choice not in ["1", "2", "3", "4"]:
                            raise NotAnOptionError
                    except NotAnOptionError: print("That's not a valid option.")

                    # Choice execution
                    match choice:
                        case "1":
                            # Ask the user to select one of the default tags
                            while True:
                                print()
                                print(f"Options -> {Task.tags_defaults}", end=", ")
                                try:
                                    user_input = input("Tag: ").strip()
                                    # Validate the user input against available default tags
                                    if not user_input:raise EmptyError
                                    elif user_input.lower() not in [tag.lower() for tag in Task.tags_defaults]:
                                        raise NotAnOptionError
                                    else:
                                        selected_tags.append(user_input)
                                        print("Tag uploaded.")
                                        add_more = input("\nDo you want to add another tag? (yes/no): ").strip().lower()
                                        if add_more != "yes": return selected_tags
                                        break
                                except EmptyError: print("This slot can't be empty.")
                                except NotAnOptionError: print("That's not a valid option.")

                        case "2":
                            while True:
                                # Ask the user to select and modify a default tag
                                print()
                                print(f"Options -> {Task.tags_defaults}", end=", ")
                                try:
                                    user_input = input("Tag: ").strip()
                                    # Validate input and ensure the selected tag is in the defaults
                                    if not user_input: raise EmptyError
                                    elif user_input.lower() not in [tag.lower() for tag in Task.tags_defaults]:
                                        raise NotAnOptionError
                                    else:
                                        # Proceed to modify the selected tag
                                        while True:
                                            try:
                                                change = input("What's the new tag version?: ").strip()
                                                if not change: raise EmptyError
                                                else: 
                                                    print(f"New tag version: '{change}'")
                                                    confirmation = input("Are you sure you want this to be the new version of the tag? (yes/no): ").strip().lower()
                                                    if confirmation == "yes":
                                                        # Find original tag
                                                        original_tag = next(tag for tag in Task.tags_defaults if tag.lower() == user_input.lower())
                                                        # Find original tag index
                                                        index = Task.tags_defaults.index(original_tag)
                                                        # Modifying original tag
                                                        Task.tags_defaults[index] = change
                                                        selected_tags.append(change)
                                                        print(f"Tag updated: {original_tag} -> {change}")
                                                        print("Tag uploaded.")
                                                        break
                                            except EmptyError: print("This slot can't be empty.")
                                        add_more = input("\nDo you want to add another tag? (yes/no): ").strip().lower()
                                        if add_more != "yes": return selected_tags
                                        break         
                                except EmptyError: print("This slot can't be empty.")
                                except NotAnOptionError: print("That's not a valid option.")

                        case "3":
                            # Ask the user to create a new tag and add it to the defaults
                            while True:
                                try:
                                    new = input("What's the new tag?: ").strip()
                                    if not new: raise EmptyError
                                    else: 
                                        print(f"New tag version: '{new}'")
                                        confirmation = input("Are you sure you want this to be the new tag? (yes/no): ").strip().lower()
                                        if confirmation == "yes":
                                            # Add the new tag to the list of default tags
                                            Task.tags_defaults.append(new)
                                            selected_tags.append(new)
                                            print("Tag uploaded.")
                                            break
                                except EmptyError: print("This slot can't be empty.")
                            add_more = input("\nDo you want to add another tag? (yes/no): ").strip().lower()
                            if add_more != "yes": return selected_tags
                            break
                        
                        case "4":
                            # No tags selected, return None
                            return None
                        
            case _: pass

class EmptyError(Exception):
    # user entered an empty input, prompt for valid input
    pass
class NotAnOptionError(Exception):
    # user entered an invalid option, prompt for valid input
    pass
