"""
task_controller.py - Controller / Business Logic Layer
Separates UI from data (MVC Pattern)
"""

from models.models import Task, User, Category


class AuthController:
    """Handles authentication logic"""

    @staticmethod
    def login(username: str, password: str):
        """
        Validate and return user; raises ValueError on failure.
        Returns: User object
        """
        if not username.strip() or not password.strip():
            raise ValueError("Username and password cannot be empty.")
        user = User.authenticate(username.strip(), password.strip())
        if not user:
            raise ValueError("Invalid username or password.")
        return user

    @staticmethod
    def register(username: str, password: str, confirm: str, email: str = ""):
        """Register a new user"""
        username = username.strip()
        password = password.strip()

        if not username or not password:
            raise ValueError("All fields are required.")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters.")
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters.")
        if password != confirm:
            raise ValueError("Passwords do not match.")
        if User.exists(username):
            raise ValueError("Username already taken. Choose another.")

        success = User.create(username, password, email)
        if not success:
            raise ValueError("Registration failed. Try again.")
        return True


class TaskController:
    """Handles all task-related operations (Business Logic)"""

    # ── Validation ──────────────────────────────
    @staticmethod
    def validate_task(title: str, priority: str, status: str) -> None:
        """Raise ValueError if task data is invalid"""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")
        if len(title.strip()) < 3:
            raise ValueError("Title must be at least 3 characters.")
        if priority not in Task.PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}")
        if status not in Task.STATUSES:
            raise ValueError(f"Invalid status: {status}")

    # ── CRUD ─────────────────────────────────────
    @staticmethod
    def add_task(user_id: int, title: str, description: str, priority: str,
                 status: str, due_date: str, category_id: int):
        TaskController.validate_task(title, priority, status)
        return Task.create(
            title=title.strip(), description=description.strip(),
            priority=priority, status=status,
            due_date=due_date if due_date else None,
            category_id=category_id, user_id=user_id
        )

    @staticmethod
    def edit_task(task_id: int, title: str, description: str, priority: str,
                  status: str, due_date: str, category_id: int):
        TaskController.validate_task(title, priority, status)
        return Task.update(
            task_id=task_id, title=title.strip(),
            description=description.strip(), priority=priority,
            status=status,
            due_date=due_date if due_date else None,
            category_id=category_id
        )

    @staticmethod
    def remove_task(task_id: int):
        if not task_id:
            raise ValueError("Invalid task ID.")
        return Task.delete(task_id)

    @staticmethod
    def get_tasks(user_id: int, status_filter=None,
                  priority_filter=None, search=None):
        return Task.get_all(user_id, status_filter, priority_filter, search)

    @staticmethod
    def get_dashboard_stats(user_id: int):
        return Task.get_stats(user_id)

    @staticmethod
    def get_categories(user_id: int):
        return Category.get_all(user_id)

    @staticmethod
    def add_category(name: str, color: str, user_id: int):
        if not name.strip():
            raise ValueError("Category name cannot be empty.")
        return Category.create(name.strip(), color, user_id)
