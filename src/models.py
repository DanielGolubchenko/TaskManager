import hashlib
from datetime import datetime

class Task:
    # Default non-modifiable variables
    priority_defaults = ("Low", "Medium", "High", "Urgent")
    status_defaults = ("Pending", "In progress", "Completed", "Canceled")

    # Default modifiable variable
    tags_defaults = ["Work", "Studies", "Home", "Meetings", "Goals", "Reading", "Shopping", "Bills"]

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
        # 🚧🚧asi pondriamos en accion la funcion task_filter. realizar condicional o funcion extra para validar los diferentes return de la funciion.
        filtered_list = TaskManager.task_filter(self.tasks_list)
    
    def modify_task(self):
        pass # 🚧🚧terminar los getter y setter privados en class Task

    def delete_task(self):
        pass

    # Validates each posible task atribute input
    @staticmethod
    def validation(value):
        match value:
            case "title":
                return TaskManager.get_valid_input("\nTitle(*): ")

            case "priority":
                # Display available options for priority selection
                print(f"\nOptions -> {Task.priority_defaults}")
                return TaskManager.get_valid_input("Priority(*): ", valid_options=["low", "medium", "high", "urgent"]).capitalize()

            case "status":
                # Display available options for status selection
                print(f"\nOptions -> {Task.status_defaults}")
                return TaskManager.get_valid_input("Status(*): ", valid_options=["pending", "in progress", "completed", "canceled"]).capitalize()
            
            case "description":
                # Get the task description (optional). If empty, return None.
                return TaskManager.get_valid_input("\nDescription (press 'Enter' to skip): ", allow_empty=True)
            
            case "due_date":
                # Prompt user for a due date (Optional and can be just a date or date with time)
                return TaskManager.get_valid_input("\nEnter due date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM), or press 'Enter' to skip: ", is_date=True, allow_empty=True)

            case "tags":
                # Initialize an empty list to store the selected tags
                selected_tags = []

                while True:
                    # Presenting the available options for tag management
                    print(f"\nOptions -> {Task.tags_defaults}")
                    print("1. Choose a default tag")
                    print("2. Modify a default tag")
                    print("3. Create a new tag")
                    print("4. Skip (no tags)")
                   
                    # Ensure the user input is one of the valid options (1-4)
                    choice = TaskManager.get_valid_input("\nEnter the number (1-4) for your choice: ", valid_options=["1", "2", "3", "4"])
                    
                    # Choice execution
                    match choice:
                        case "1":
                            # Ask the user to select one of the default tags
                            print(f"\nOptions -> {Task.tags_defaults}")
                            user_input = TaskManager.get_valid_input("Tag: ", valid_options=[tag.lower() for tag in Task.tags_defaults]).capitalize()
                            # Tag upload
                            selected_tags.append(user_input)
                            print("Tag uploaded.")
                            # Asking for more tags
                            add_more = input("\nDo you want to add another tag? (yes/no): ").strip().lower()
                            if add_more != "yes": return selected_tags

                        case "2":
                            # Ask the user to select and modify a default tag
                            print(f"\nOptions -> {Task.tags_defaults}")
                            # Validate input and ensure the selected tag is in the defaults
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
                                    # Add the new tag to the list of default tags
                                    Task.tags_defaults.append(new)
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
        # Create a copy of the tasks_list to manipulate without affecting the original list
        filtered_list = tasks_list[:]

        # Define the available filter options
        options = ["title", "priority", "status", "due_date", "created_at", "tags"]
        
        # Function to filter tasks based on a user's input for a specific attribute
        def match_locator(user_input, attribute, filtered_list):
            filtered_list = [task for task in filtered_list if user_input in str(getattr(task, attribute, "")).lower()]
            if filtered_list:
                print("Match achieved.")
                return filtered_list
            else:
                print("No match was achieved.")
                return None

        # Display the filter options to the user
        print(f"\nThese are the possible filter options:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        # Ask the user to select a filter option (1-6)
        choice = TaskManager.get_valid_input("\nEnter the number (1-6) for your choice: ", valid_options=["1", "2", "3", "4", "5", "6"])

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
                return match_locator(user_input, "_priority", filtered_list)

            # Status filter
            case "3":
                print(f"\nOptions -> {Task.status_defaults}")
                user_input = TaskManager.get_valid_input("\nWhat status would you like to search for? ", valid_options=["pending", "in progress", "completed", "canceled"])
                return match_locator(user_input, "_status", filtered_list)

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

    # Function to get valid input from the user, handles empty input, invalid options, and date format
    @staticmethod
    def get_valid_input(prompt, valid_options=None, is_date=False, allow_empty=False):
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
    # user entered an empty input, prompt for valid input
    def __init__(self, message="This slot can't be empty."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

class NotAnOptionError(Exception):
    # user entered an invalid option, prompt for valid input
    def __init__(self, message="That's not a valid option."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
