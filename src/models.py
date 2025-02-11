import hashlib
from datetime import datetime

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
        attribute_index = TaskManager.get_valid_input("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])
        
        # Get the attribute name corresponding to the selected number
        attribute_name = options[int(attribute_index) - 1].lower()
        
        # Receive modification value for the selected attribute
        modification = TaskManager.attribute_validation(attribute_name)
        
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

        title = TaskManager.attribute_validation("title")
        priority = TaskManager.attribute_validation("priority")
        status = TaskManager.attribute_validation("status")
        description = TaskManager.attribute_validation("description")
        due_date = TaskManager.attribute_validation("due_date")
        tags = TaskManager.attribute_validation("tags")

        task = Task(title, priority, status, description, due_date, tags)
        self.tasks_list.append(task)
        print("Task added succesfully!")

    def show_tasks(self):
        tasks = self.tasks_list

        if len(tasks) >= 2:
            # Ask if the user wants to filter the task list
            by_filter = TaskManager.get_valid_input("Do you want to display the task list with a specific filter? (yes/no): ")
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
    
        for task in filtered_list:
            print(task)

        action = TaskManager.get_valid_input("Do you want to modify or delete a task? (modify/delete/no): ", valid_options=["modify", "delete", "no"])

        if action in ["modify", "delete"]:
            if len(filtered_list) == 1:
                task = filtered_list[0]  # Directly select the only task
                print(f"\nSelected task:\n{task}") 
            else:
                print("\nSelect a task to proceed:")
                for task in filtered_list:
                    print(task) 

                task_ids = [task.task_id for task in filtered_list]  # Get task IDs
                task_id = TaskManager.get_valid_input("Enter the ID of the task: ", valid_options=task_ids)
                task = next(task for task in filtered_list if task.task_id == task_id)  # Find the selected task

            if action == "modify":
                task.modify_task()
            else:
                self.tasks_list.remove(task)
                print("Task deleted successfully.")
    
    @staticmethod
    def attribute_validation(value):
        """Validates each posible task atribute input"""

        match value:
            case "title":
                return TaskManager.get_valid_input("\nTitle(*): ")

            case "priority":
                print(f"\nOptions -> {Task.priority_defaults}")
                return TaskManager.get_valid_input("Priority(*): ", valid_options=["low", "medium", "high", "urgent"]).capitalize()

            case "status":
                print(f"\nOptions -> {Task.status_defaults}")
                return TaskManager.get_valid_input("Status(*): ", valid_options=["pending", "in progress", "completed", "canceled"]).capitalize()
            
            case "description":
                return TaskManager.get_valid_input("\nDescription (press 'Enter' to skip): ", allow_empty=True)
            
            case "due_date":
                return TaskManager.get_valid_input("\nEnter due date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM), or press 'Enter' to skip: ", is_date=True, allow_empty=True)

            case "tags":
                selected_tags = []

                while True:
                    print(f"\nOptions -> {Task.tags_defaults}")
                    print("1. Choose a default tag")
                    print("2. Modify a default tag")
                    print("3. Create a new tag")
                    print("4. Skip (no tags)")
                   
                    choice = TaskManager.get_valid_input("\nEnter the number (1-4) for your choice: ", valid_options=["1", "2", "3", "4"])
                    
                    # Choice execution
                    match choice:
                        case "1":
                            print(f"\nOptions -> {Task.tags_defaults}")
                            user_input = TaskManager.get_valid_input("Tag: ", valid_options=[tag.lower() for tag in Task.tags_defaults]).capitalize()
                            
                            selected_tags.append(user_input) # Tag upload
                            print("Tag uploaded.")

                            add_more = input("\nDo you want to add another tag? (yes/no): ").strip().lower()
                            if add_more != "yes": return selected_tags

                        case "2":
                            print(f"\nOptions -> {Task.tags_defaults}")
                            user_input = TaskManager.get_valid_input("Tag: ", valid_options=[tag.lower() for tag in Task.tags_defaults])
                            
                            # Proceed to modify the selected tag
                            while True:
                                change = TaskManager.get_valid_input("What's the new tag version?: ")
                                
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
                            add_more = input("\nDo you want to add another tag? (yes/no): ").strip().lower()
                            if add_more != "yes": return selected_tags       

                        case "3":
                            # Ask the user to create a new tag and add it to defaults
                            while True:
                                new = TaskManager.get_valid_input("What's the new tag?: ")
                                print(f"New tag version: '{new}'")
                                confirmation = input("Are you sure you want this to be the new tag? (yes/no): ").strip().lower()
                                if confirmation == "yes":
                                    Task.tags_defaults.append(new) # Add the new tag to the list of default tags
                                    selected_tags.append(new)
                                    print("Tag uploaded.")
                                    break
                            add_more = input("\nDo you want to add another tag? (yes/no): ").strip().lower()
                            if add_more != "yes": return selected_tags

                        case "4":
                            # No tags selected, return None
                            return None

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
                return filtered_list
            else:
                print("No match was achieved.\n")
                return None

        print(f"\nThese are the possible filter options:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = TaskManager.get_valid_input("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])

        # Perform the filtering action based on the user's choice
        match choice:
            # Title filter
            case "1":
                user_input = TaskManager.get_valid_input("\nWhat title would you like to search for? ")
                return match_locator(user_input, "title", filtered_list)
            
            # Priority filter
            case "2":
                print(f"\nOptions -> {Task.priority_defaults}")
                user_input = TaskManager.get_valid_input("\nWhat priority would you like to search for? ", valid_options=["low", "medium", "high", "urgent"])
                return match_locator(user_input, "priority", filtered_list)

            # Status filter
            case "3":
                print(f"\nOptions -> {Task.status_defaults}")
                user_input = TaskManager.get_valid_input("\nWhat status would you like to search for? ", valid_options=["pending", "in progress", "completed", "canceled"])
                return match_locator(user_input, "status", filtered_list)

            # Due date filter
            case "4":
                user_input = TaskManager.get_valid_input("\nEnter due date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM): ", is_date=True)
                return match_locator(str(user_input), "due_date", filtered_list)
            
            # Created date filter
            case "5":
                user_input = TaskManager.get_valid_input("\nEnter created date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM): ", is_date=True)
                return match_locator(str(user_input), "created_at", filtered_list)
            
            # Tags filter
            case "6":
                print(f"\nOptions -> {Task.tags_defaults}")
                user_input = TaskManager.get_valid_input("\nWhat tag would you like to search for? ", valid_options=[tag.lower() for tag in Task.tags_defaults])
                return match_locator(user_input, "tags", filtered_list)

    @staticmethod
    def get_valid_input(prompt, valid_options=None, is_date=False, allow_empty=False):
        """Function to get valid input from the user, handles empty input, invalid options, and date format"""

        while True:
            try:
                user_input = input(prompt).strip().lower()
                
                # If empty input is allowed and the user provides an empty input, return None
                if allow_empty and not user_input:
                    return None
                
                # Check if the input is empty and raise an error
                if not user_input:
                    raise EmptyError()
                
                # Handle date input and convert to appropriate format
                if is_date:
                    if " " in user_input:
                        return datetime.strptime(user_input, "%d-%m-%Y %H:%M")
                    else:
                        return datetime.strptime(user_input, "%d-%m-%Y").date()
                
                # Validate if the input matches one of the valid options
                if valid_options and user_input not in valid_options:
                    raise NotAnOptionError()
                return user_input
            except EmptyError:
                pass
            except NotAnOptionError:
                pass
            except ValueError:
                print("Invalid format. Use 'DD-MM-YYYY' or 'DD-MM-YYYY HH:MM'.")

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
