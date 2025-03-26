
# TaskManager

TaskManager is a web application designed to help users efficiently manage their personal tasks. It offers the ability to create, update, and delete tasks while keeping track of their progress.

---

## Features

- **User Authentication**: Users can create an account, log in, and manage their personal tasks.
- **Task Management**: Tasks can be created, updated, and deleted by the user.
- **Priority Levels**: Each task can be assigned a priority level: `Low`, `Medium`, `High`, or `Urgent`.
- **Task Statuses**: Users can set a task's status to one of the following:
  - **Pending**
  - **In Progress**
  - **Completed**
  - **Canceled**
- **Due Dates**: Tasks can have deadlines, helping users keep track of when tasks need to be completed.
- **Tags**: Tasks can be tagged for better organization and filtering.
- **Account Management**: Users can easily sign up, log in, and manage their tasks.

---

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **Database**: SQLite (default, but can be switched to PostgreSQL, MySQL, etc.)

---

## Installation

### Requirements

- Python 3.8 or higher
- Django 5.x

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/DanielGolubchenko/TaskManager.git
   cd TaskManager
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional) to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Open your browser and go to `http://127.0.0.1:8000/` to start using the app.

---

## Usage

- **Sign Up / Log In**: Users can sign up and log in to manage their tasks.
- **Task Creation**: Once logged in, users can create tasks by providing a title, description, due date, and priority.
- **Task Status**: Users can update a task's status to Completed, Canceled, In Progress, or Pending.
- **Task Management**: Users can edit or delete their tasks as needed.

---

## Contributing

Contributions are welcome! If you'd like to improve the project, feel free to fork this repository, make changes, and submit a pull request. You can also report issues by opening an issue in the GitHub repository.

### Contribution Steps:
1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a pull request

---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.md) file for more details.

---

## Acknowledgements

- The Django documentation for providing such a powerful and flexible web framework.
- [SQLite](https://www.sqlite.org/) for offering a simple and lightweight database solution.