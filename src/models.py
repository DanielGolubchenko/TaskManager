import hashlib
from datetime import datetime
from controllers import get_valid_input
from controllers import attribute_validation

class Task:
    """
    Represents a task with attributes like title, priority, status, and due date.
    Provides methods to modify, display, and manage tasks.
    """

    # Default non-modifiable priority and status values
    priority_defaults = ("Low", "Medium", "High", "Urgent")
    status_defaults = ("Pending", "In progress", "Completed", "Canceled")

    # Default modifiable tags values
    tags_defaults = ["Work", "Studies", "Home", "Meetings", "Goals", "Reading", "Shopping", "Bills"]

    def __init__(self, title, priority, status, description=None, due_date=None, created_at=None, updated_at=None, tags=None, task_id=None):
        self.title = title
        self.priority = priority
        self.status = status 
        self.description = description if description is not None else []
        self.due_date = due_date if due_date is not None else []
        self.created_at = created_at if created_at is not None else datetime.now().strftime("%d/%m/%Y %H:%M")
        self.updated_at = updated_at if updated_at is not None else datetime.now().strftime("%d/%m/%Y %H:%M")
        self.tags = tags if tags is not None else [] 
        self.task_id = task_id if task_id is not None else self.generate_task_id()

    def generate_task_id(self):
        """Operates only at task creation"""
        data = (self.title + str(self.created_at)).encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    def __str__(self):
        """Returns a formatted string representation of the task object, displaying all attributes and their values."""
        task_info = vars(self)
        info_str = "\n----TASK----\n"
        for k, v in task_info.items():
            if "_" in k:
                k = k.replace("_", " ")
            info_str += f"{k.capitalize()}: {v}\n"
        return info_str

    def modify_task(self):
        """Allows the user to modify an attribute of the task."""

        options = ["Title", "Priority", "Status", "Description", "Due_date", "Tags"]

        print(f"\nThese are the modifiable options:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        # Prompt to select an attribute
        attribute_index = get_valid_input("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])
        
        # Get the attribute name corresponding to the selected number
        attribute_name = options[int(attribute_index) - 1].lower()
        
        # Receive modification value for the selected attribute
        modification = attribute_validation(attribute_name)
        
        # Dynamically assign the new value to the corresponding attribute
        setattr(self, attribute_name, modification)
        
        # Update the timestamp whenever a modification is made
        self.updated_at = datetime.now().strftime("%d/%m/%Y %H:%M")

        print("Task updated successfully.")

class TaskManager:
    """A class responsible for managing tasks, including creation, modification, deletion and filtering."""

    def __init__(self, name="task_manager", ):
        self.name = name
        self.tasks_list = []

    def add_task(self):
        print("Those entries with the symbol (*) are mandatory.")

        title = attribute_validation("title")
        priority = attribute_validation("priority")
        status = attribute_validation("status")
        description = attribute_validation("description")
        due_date = attribute_validation("due_date")
        tags = attribute_validation("tags")

        task = Task(title, priority, status, description, due_date, tags=tags)
        self.tasks_list.append(task)
        print("Task added succesfully!")

    def show_tasks(self):
        tasks = self.tasks_list

        if len(tasks) >= 2:
            # Ask if the user wants to filter the task list
            by_filter = get_valid_input("Do you want to display the task list with a specific filter? (yes/no): ")
            if by_filter == "yes":
                # Apply filter; if None is returned, use an empty list
                tasks = TaskManager.task_filter(tasks) or []
        
        # Print each task in the final list (filtered or not)
        for task in tasks:
            print(task)

    def find_and_modify_or_delete_task(self):
        """Finds a task and allows the user to modify or delete it."""

        filtered_list = TaskManager.task_filter(self.tasks_list) or []
        
        if not filtered_list:
            return
        
        if len(filtered_list) == 1: # If only one task is found, select it automatically
            task = filtered_list[0]
        else:
            print("\nSelect a task to proceed:")
            for task in filtered_list:  # Display the filtered list of tasks
                print(task)
            
            task_ids = [task.task_id for task in filtered_list] # Get the task IDs for validation
            task_id = get_valid_input("Enter the ID of the task: ", valid_options=task_ids) # Ensure the user selects a valid task ID
            task = next(task for task in filtered_list if task.task_id == task_id)

        print(f"\nSelected task:\n{task}")

        action = get_valid_input("Do you want to modify or delete this task? (modify/delete/no): ", valid_options=["modify", "delete", "no"])
        
        # Perform the selected action
        if action == "modify":
            task.modify_task()
        elif action == "delete":
            self.tasks_list = [t for t in self.tasks_list if t.task_id != task.task_id]
            print("Task deleted successfully.")
        else:
            print("No action taken.")

    @staticmethod
    def task_filter(tasks_list):
        """Filters tasks based on specified criteria such as priority, status, and tags."""

        filtered_list = tasks_list[:]
        options = ["Title", "Priority", "Status", "Due date", "Created_at", "Tags"]
        
        def match_locator(user_input, attribute, filtered_list):
            """Searches for a match between the user's input and the attribute value of each task in the filtered list."""

            filtered_list = [task for task in filtered_list if user_input in str(getattr(task, attribute, "")).lower()]
            if filtered_list:
                print("Match achieved.\n")
            else:
                print("No match was achieved.\n")
            return []

        print(f"\nThese are the possible filter options:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = get_valid_input("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])

        # Perform the filtering action based on the user's choice
        match choice:
            # Title filter
            case "1":
                user_input = get_valid_input("\nWhat title would you like to search for? ")
                return match_locator(user_input, "title", filtered_list)
            
            # Priority filter
            case "2":
                print(f"\nOptions -> {Task.priority_defaults}")
                user_input = get_valid_input("\nWhat priority would you like to search for? ", valid_options=["low", "medium", "high", "urgent"])
                return match_locator(user_input, "priority", filtered_list)

            # Status filter
            case "3":
                print(f"\nOptions -> {Task.status_defaults}")
                user_input = get_valid_input("\nWhat status would you like to search for? ", valid_options=["pending", "in progress", "completed", "canceled"])
                return match_locator(user_input, "status", filtered_list)

            # Due date filter
            case "4":
                user_input = get_valid_input("\nEnter due date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM): ", is_date=True)
                return match_locator(str(user_input), "due_date", filtered_list)
            
            # Created date filter
            case "5":
                user_input = get_valid_input("\nEnter created date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM): ", is_date=True)
                return match_locator(str(user_input), "created_at", filtered_list)
            
            # Tags filter
            case "6":
                print(f"\nOptions -> {Task.tags_defaults}")
                user_input = get_valid_input("\nWhat tag would you like to search for? ", valid_options=[tag.lower() for tag in Task.tags_defaults])
                return match_locator(user_input, "tags", filtered_list)

class EmptyError(Exception):
    """Manages empty inputs"""
    def __init__(self, message="This slot can't be empty."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

class NotAnOptionError(Exception):
    """Manages invalid options"""
    def __init__(self, message="That's not a valid option."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
