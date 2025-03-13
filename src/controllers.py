from datetime import datetime

def attribute_validation(value):
    """Validates each posible task atribute input"""
    from models import Task
    match value:
        case "title":
            return get_valid_input("\nTitle(*): ")

        case "priority":
            print(f"\nOptions -> {Task.priority_defaults}")
            return get_valid_input("Priority(*): ", valid_options=["low", "medium", "high", "urgent"]).capitalize()

        case "status":
            print(f"\nOptions -> {Task.status_defaults}")
            return get_valid_input("Status(*): ", valid_options=["pending", "in progress", "completed", "canceled"]).capitalize()
        
        case "description":
            return get_valid_input("\nDescription (press 'Enter' to skip): ", allow_empty=True)
        
        case "due_date":
            return get_valid_input("\nEnter due date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM), or press 'Enter' to skip: ", is_date=True, allow_empty=True)

        case "tags":
            selected_tags = []

            while True:
                print(f"\nOptions -> {Task.tags_defaults}")
                print("1. Choose a default tag")
                print("2. Modify a default tag")
                print("3. Create a new tag")
                print("4. Skip (no tags)")
                
                choice = get_valid_input("\nEnter the number (1-4) for your choice: ", valid_options=["1", "2", "3", "4"])
                
                # Choice execution
                match choice:
                    case "1":
                        print(f"\nOptions -> {Task.tags_defaults}")
                        user_input = get_valid_input("Tag: ", valid_options=[tag.lower() for tag in Task.tags_defaults]).capitalize()
                        
                        selected_tags.append(user_input) # Tag upload
                        print("Tag uploaded.")

                        add_more = input("\nDo you want to add another tag? (yes/no): ").strip().lower()
                        if add_more != "yes": return selected_tags

                    case "2":
                        print(f"\nOptions -> {Task.tags_defaults}")
                        user_input = get_valid_input("Tag: ", valid_options=[tag.lower() for tag in Task.tags_defaults])
                        
                        # Proceed to modify the selected tag
                        while True:
                            change = get_valid_input("What's the new tag version?: ")
                            
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
                            new = get_valid_input("What's the new tag?: ")
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
                    
def get_valid_input(prompt, valid_options=None, is_date=False, allow_empty=False):
    """Function to get valid input from the user, handles empty input, invalid options, and date format"""
    from models import EmptyError
    from models import NotAnOptionError
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
