import pytest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import models
from datetime import datetime
import hashlib

class TestTask:
    @pytest.fixture
    def task_fixture(self):
        """Fixture that provides a sample Task instance with predefined attributes."""

        return models.Task(
        title="Title",
        priority="Medium",
        status="In progress",
        description="Description",
        due_date="21/03/2025 12:00",
        created_at="19/03/2025 12:00",
        updated_at="20/03/2025 12:00",
        tags=["Work"],
        task_id="#id")
    
    
    def test_create_task(self, task_fixture):
        """Tests that a Task instance is correctly initialized with given attributes."""

        assert task_fixture.title == "Title"
        assert task_fixture.priority == "Medium"
        assert task_fixture.status == "In progress"
        assert task_fixture.description == "Description"
        assert task_fixture.due_date == "21/03/2025 12:00"
        assert task_fixture.created_at == "19/03/2025 12:00"
        assert task_fixture.updated_at == "20/03/2025 12:00"
        assert task_fixture.tags == ["Work"]
        assert task_fixture.task_id == "#id"

        # Test: default created_at should be set to the current timestamp
        task = models.Task(title="Title", priority="Medium", status="In progress")
        assert task.created_at == datetime.now().strftime("%d/%m/%Y %H:%M")

        # Test: default updated_at should match created_at at initialization
        assert task.updated_at == datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def test_generate_task_id(self):
        """Tests that the generate_task_id method produces the correct hash based on title and created_at."""

        title = "Test Task"
        created_at = "19/03/2025 12:00"

        expected_task_id = hashlib.sha256((title + created_at).encode('utf-8')).hexdigest()

        task = models.Task(title=title, priority="Medium", status="In progress", created_at=created_at)

        assert task.task_id == expected_task_id

    def test_task_str_method(self, task_fixture):
        """Tests that the __str__ method returns the expected formatted string representation of the task."""

        expected_str = (
            "\n----TASK----\n"
            f"Title: {task_fixture.title}\n"
            f"Priority: {task_fixture.priority}\n"
            f"Status: {task_fixture.status}\n"
            f"Description: {task_fixture.description}\n"
            f"Due date: {task_fixture.due_date}\n"
            f"Created at: {task_fixture.created_at}\n"
            f"Updated at: {task_fixture.updated_at}\n"
            f"Tags: {task_fixture.tags}\n"
            f"Task id: {task_fixture.task_id}\n"
        )

        assert str(task_fixture) == expected_str
    
    @patch("models.get_valid_input", return_value="1")
    @patch("models.attribute_validation", return_value="New Title")
    def test_modify_task(self, mock_attribute_validation, mock_get_valid_input, task_fixture):
        """
        Tests that modify_task correctly updates the selected attribute 
        and updates the timestamp.
        """
        prev_updated_at = task_fixture.updated_at

        task_fixture.modify_task()

        # Ensure get_valid_input was called correctly
        mock_get_valid_input.assert_called_once_with("\nEnter the number (1-6) for your choice: ", valid_options=["1", "2", "3", "4", "5", "6"])
        
        # Ensure attribute_validation was called correctly
        mock_attribute_validation.assert_called_once_with("title")

        # Check if the attribute was updated correctly
        assert task_fixture.title == "New Title"
        
        # Check if the updated_at timestamp was modified
        assert task_fixture.updated_at != prev_updated_at
        assert task_fixture.updated_at == datetime.now().strftime("%d/%m/%Y %H:%M")

    @patch("models.get_valid_input", return_value="5")
    @patch("models.attribute_validation", return_value="22/03/2025 14:00")
    def test_modify_task_due_date(self, mock_attribute_validation, mock_get_valid_input, task_fixture):
        """Test modifying the due_date attribute of a task."""
        
        prev_updated_at = task_fixture.updated_at  # Store previous updated_at timestamp

        task_fixture.modify_task()  # Call the method to modify the task

        # Ensure that get_valid_input was called with the correct prompt and options
        mock_get_valid_input.assert_called_once_with("\nEnter the number (1-6) for your choice: ", valid_options=["1", "2", "3", "4", "5", "6"])
        
        # Ensure that attribute_validation was called with "due_date"
        mock_attribute_validation.assert_called_once_with("due_date")

        # Validate that the due_date attribute was updated correctly
        assert task_fixture.due_date == "22/03/2025 14:00"

        # Ensure that the updated_at timestamp has changed
        assert task_fixture.updated_at != prev_updated_at
        assert task_fixture.updated_at == datetime.now().strftime("%d/%m/%Y %H:%M")

class TestTaskManager:
    def test_create_task_manager(self):
        """Test that a TaskManager instance is correctly initialized with an empty tasks_list attribute."""

        task_manager = models.TaskManager()

        assert task_manager.name == "task_manager"
        assert task_manager.tasks_list == []

    @patch("models.attribute_validation", side_effect=["Title", "Medium", "In progress", "Description", "21/03/2025 12:00", ["Work"]])
    def test_add_task(self, mock_attribute_validation):
        """Test that a task is correctly added to the tasks_list of a TaskManager instance."""
        
        task_manager = models.TaskManager()
        
        assert len(task_manager.tasks_list) == 0
        
        task_manager.add_task()
        
        # Ensure that the tasks_list attribute has been updated
        assert len(task_manager.tasks_list) == 1

        task = task_manager.tasks_list[0]
        
        # Validate that the task was created with the correct attributes
        assert task.title == "Title"
        assert task.priority == "Medium"
        assert task.status == "In progress"
        assert task.description == "Description"
        assert task.due_date == "21/03/2025 12:00"
        assert task.tags == ["Work"]
        
        # Ensure that attribute_validation was called 6 times
        assert mock_attribute_validation.call_count == 6

    @patch("builtins.print")
    @patch("models.get_valid_input", return_value="yes")
    @patch("models.TaskManager.task_filter", return_value=[models.Task(title="Title", priority="Medium", status="In progress", description="Description", due_date="21/03/2025 12:00", tags=["Work"])])
    def test_show_tasks_filtered(self, mock_task_filter, mock_get_valid_input, mock_print):
        """Test that the show_tasks method correctly filters and displays tasks."""
        
        task_manager = models.TaskManager()
        task_manager.tasks_list = [models.Task(title="Title", priority="Medium", status="In progress", description="Description", due_date="21/03/2025 12:00", tags=["Work"]),
                                   models.Task(title="Title 2", priority="Low", status="To do", description="Description 2", due_date="22/03/2025 12:00", tags=["Personal"])]

        task_manager.show_tasks()

        # Ensure that get_valid_input was called with the correct prompt
        mock_get_valid_input.assert_called_once_with("Do you want to display the task list with a specific filter? (yes/no): ")

        # Ensure that task_filter was called with the correct argument
        mock_task_filter.assert_called_once_with(task_manager.tasks_list)

        # Ensure that the filtered task was printed
        mock_print.assert_called_once_with(mock_task_filter.return_value[0])

    @patch("builtins.print")
    @patch("models.get_valid_input", return_value="modify")
    @patch("models.TaskManager.task_filter", return_value=[models.Task(title="Title", priority="Medium", status="In progress", description="Description", due_date="21/03/2025 12:00", tags=["Work"])] )
    @patch("models.Task.modify_task")
    def test_find_and_modify_task(self, mock_modify_task, mock_task_filter, mock_get_valid_input, mock_print):
        """Test that a task is correctly modified when selected by the user."""
        
        task_manager = models.TaskManager()
        task_manager.tasks_list = [models.Task(title="Title", priority="Medium", status="In progress", description="Description", due_date="21/03/2025 12:00", tags=["Work"]),
                                   models.Task(title="Title 2", priority="Low", status="To do", description="Description 2", due_date="22/03/2025 12:00", tags=["Personal"])]

        task_manager.find_and_modify_or_delete_task()

        # Ensure that get_valid_input was called with the correct prompt and options
        mock_get_valid_input.assert_called_once_with("Do you want to modify or delete this task? (modify/delete/no): ", valid_options=["modify", "delete", "no"])

        # Ensure that task_filter was called with the correct argument
        mock_task_filter.assert_called_once_with(task_manager.tasks_list)

        # Ensure that modify_task was called
        mock_modify_task.assert_called_once()

        # Ensure that the task was not modified
        assert task_manager.tasks_list[0].title == "Title"
        
        # Ensure that the task was printed
        mock_print.assert_called_once_with(f"\nSelected task:\n{task_manager.tasks_list[0].__str__()}")


    @patch("builtins.print")
    @patch("models.get_valid_input", return_value="delete")
    @patch("models.TaskManager.task_filter", return_value=[models.Task(task_id="1", title="Title", priority="Medium", status="In progress", description="Description", due_date="21/03/2025 12:00", tags=["Work"])])
    def test_find_and_delete_task(self, mock_task_filter, mock_get_valid_input, mock_print):
        """Test that a task is correctly deleted when selected by the user."""
        
        task_manager = models.TaskManager()
        task_manager.tasks_list = [models.Task(task_id="1", title="Title", priority="Medium", status="In progress", description="Description", due_date="21/03/2025 12:00", tags=["Work"]),
                                   models.Task(task_id="2", title="Title 2", priority="Low", status="To do", description="Description 2", due_date="22/03/2025 12:00", tags=["Personal"])]

        task_manager.find_and_modify_or_delete_task()

        # Ensure that get_valid_input was called with the correct prompt and options
        mock_get_valid_input.assert_called_once_with("Do you want to modify or delete this task? (modify/delete/no): ", valid_options=["modify", "delete", "no"])

        # Ensure that task_filter was called with the correct arguments
        mock_task_filter.assert_called_once_with(task_manager.tasks_list)

        # Ensure that the task was deleted
        assert len(task_manager.tasks_list) == 1

        # Ensure that the correct task was deleted
        assert task_manager.tasks_list[0].title == "Title 2"
        
        mock_print.assert_any_call(f"\nSelected task:\n{task_manager.tasks_list[0].__str__()}")

        # Ensure that the task was printed
        mock_print.assert_any_call("Task deleted successfully.")

    @patch("builtins.print")
    @patch("models.get_valid_input", side_effect=["1", "no"]) 
    @patch("models.TaskManager.task_filter", return_value=[models.Task(title="Title", priority="Medium", status="In progress", description="Description", due_date="21/03/2025 12:00", tags=["Work"], task_id="1"),
                                                        models.Task(title="Title 2", priority="Low", status="To do", description="Description 2", due_date="22/03/2025 12:00", tags=["Personal"], task_id="2")])
    def test_find_and_no_action(self, mock_task_filter, mock_get_valid_input, mock_print):
        """Test that no action is taken when the user selects 'no'."""
        
        task_manager = models.TaskManager()
        task_manager.tasks_list = [models.Task(title="Title", priority="Medium", status="In progress", description="Description", due_date="21/03/2025 12:00", tags=["Work"], task_id="1"),
                                models.Task(title="Title 2", priority="Low", status="To do", description="Description 2", due_date="22/03/2025 12:00", tags=["Personal"], task_id="2")]

        task_manager.find_and_modify_or_delete_task()

        mock_print.assert_any_call(f"\nSelect a task to proceed:")

        mock_get_valid_input.assert_any_call("Enter the ID of the task: ", valid_options=["1", "2"])

        mock_task_filter.assert_called_once_with(task_manager.tasks_list)

        selected_task = next(task for task in task_manager.tasks_list if task.task_id == "1")
        assert selected_task.title == "Title"
        assert selected_task.task_id == "1"

        mock_print.assert_any_call(f"\nSelected task:\n{selected_task}")

        mock_get_valid_input.assert_any_call("Do you want to modify or delete this task? (modify/delete/no): ", valid_options=["modify", "delete", "no"])
        
        mock_print.assert_any_call("No action taken.")

class TestTaskFilter:
    @pytest.fixture
    def task_list(self):
        return [
            models.Task(title="Title 1", priority="High", status="Open", due_date="2025-01-01", created_at="2025-01-01"),
            models.Task(title="Title 2", priority="Medium", status="In Progress", due_date="2025-02-01", created_at="2025-01-02"),
            models.Task(title="Another Title", priority="Low", status="Closed", due_date="2025-03-01", created_at="2025-01-03")
        ]

    @patch("models.get_valid_input", return_value="Title 2")
    def test_filter_by_title(self, mock_get_input, task_list):
        result = models.TaskManager.task_filter(task_list)
        
        assert len(result) == 1
        assert result[0].title.lower() == "title 2"

        mock_get_input.assert_any_call("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])
        mock_get_input.assert_any_call("\nWhat title would you like to search for? ")


    @patch("models.get_valid_input", return_value=["1", "title 4"])
    def test_filter_by_title_no_match(self, mock_get_input, task_list):
        result = models.TaskManager.task_filter(task_list)
        # Ensure that no task was returned
        assert result == []
        mock_get_input.assert_any_call("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])
        mock_get_input.assert_any_call("\nWhat title would you like to search for? ")


    @patch("models.get_valid_input", return_value=["2", "low"])
    def test_filter_by_priority(self, mock_get_input, task_list):
        result = models.TaskManager.task_filter(task_list)
        # Ensure that the correct task was returned
        assert result[0].priority.lower() == "low"
        mock_get_input.assert_any_call("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])
        mock_get_input.assert_any_call("\nWhat priority would you like to search for? ", valid_options=["low", "medium", "high", "urgent"])


    @patch("models.get_valid_input", return_value=["3", "to do"])
    def test_filter_by_status(self, mock_get_input, task_list):
        result = models.TaskManager.task_filter(task_list)
        # Ensure that the correct task was returned
        assert result[0].status.lower() == "to do"
        mock_get_input.assert_any_call("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])
        mock_get_input.assert_any_call("\nWhat status would you like to search for? ", valid_options=["pending", "in progress", "completed", "canceled"])


    @patch("models.get_valid_input", return_value=["4", "22/03/2025 12:00"])
    def test_filter_by_due_date(self, mock_get_input, task_list):
        result = models.TaskManager.task_filter(task_list)
        # Ensure that the correct task was returned
        assert result[0].due_date == "22/03/2025 12:00"
        mock_get_input.assert_any_call("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])
        mock_get_input.assert_any_call("\nEnter due date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM): ", is_date=True)
    

    @patch("models.get_valid_input", return_value=["5", "05/02/2025 12:00"])
    def test_filter_by_created_at(self, mock_get_input, task_list):
        result = models.TaskManager.task_filter(task_list)
        # Ensure that the correct task was returned
        assert result[0].created_at == "05/02/2025 12:00"
        mock_get_input.assert_any_call("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])
        mock_get_input.assert_any_call("\nEnter created date (DD-MM-YYYY) or (DD-MM-YYYY HH:MM): ", is_date=True)


    @patch("models.get_valid_input", return_value=["6", "personal"])
    def test_filter_by_tags(self, mock_get_input, task_list):
        result = models.TaskManager.task_filter(task_list)
        # Ensure that the correct task was returned
        assert result[0].tags == ["Personal"]
        mock_get_input.assert_any_call("\nEnter the number (1-6) for your choice: ", valid_options=[str(i) for i in range(1, 7)])

class TestEmptyError:
    def test_empty_error(self):
        """Test that an EmptyError instance is correctly initialized with a default message."""
        with pytest.raises(models.EmptyError) as exc_info:
            raise models.EmptyError()
        assert str(exc_info.value) == "This slot can't be empty."

class TestNotAnOptionError:
    def test_not_an_option_error(self):
        """Test that a NotAnOptionError instance is correctly initialized with a default message."""
        with pytest.raises(models.NotAnOptionError) as exc_info:
            raise models.NotAnOptionError()
        assert str(exc_info.value) == "That's not a valid option."