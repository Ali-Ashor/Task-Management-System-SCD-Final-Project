"""
tests/test_task_manager.py
Unit Tests for Task Management System using PyTest
Tests: Models, Controllers, Validation, Edge Cases
Run: pytest tests/ -v
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.models import Task, User, Category
from controllers.task_controller import AuthController, TaskController


# ══════════════════════════════════════════════
#  FIXTURES
# ══════════════════════════════════════════════

@pytest.fixture(scope="module")
def test_user():
    """Create a test user and return it; cleanup after module tests"""
    username = "pytest_user_001"
    # Remove if exists
    from models.database import TaskManagerDB
    db = TaskManagerDB()
    with db as d:
        d.cursor.execute("DELETE FROM users WHERE username=?", (username,))
    User.create(username, "test1234", "pytest@test.com")
    user = User.authenticate(username, "test1234")
    yield user
    # Cleanup
    with db as d:
        d.cursor.execute("DELETE FROM tasks WHERE user_id=?", (user.id,))
        d.cursor.execute("DELETE FROM users WHERE id=?", (user.id,))


@pytest.fixture
def sample_task_id(test_user):
    """Create a sample task and return its id; delete after test"""
    cats = TaskController.get_categories(test_user.id)
    cat_id = cats[0].id if cats else None
    task_id = TaskController.add_task(
        user_id=test_user.id,
        title="Fixture Test Task",
        description="Created by pytest fixture",
        priority="Medium",
        status="Pending",
        due_date="2025-12-31",
        category_id=cat_id
    )
    yield task_id
    # Teardown
    try:
        TaskController.remove_task(task_id)
    except Exception:
        pass


# ══════════════════════════════════════════════
#  AUTH CONTROLLER TESTS
# ══════════════════════════════════════════════

class TestAuthController:

    def test_login_valid_credentials(self):
        """Login with correct username/password returns User"""
        user = AuthController.login("admin", "admin123")
        assert user is not None
        assert user.username == "admin"

    def test_login_invalid_password(self):
        """Login with wrong password raises ValueError"""
        with pytest.raises(ValueError, match="Invalid username or password"):
            AuthController.login("admin", "wrongpassword")

    def test_login_nonexistent_user(self):
        """Login with non-existent user raises ValueError"""
        with pytest.raises(ValueError):
            AuthController.login("ghost_user_xyz", "anypassword")

    def test_login_empty_username(self):
        """Empty username raises ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            AuthController.login("", "admin123")

    def test_login_empty_password(self):
        """Empty password raises ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            AuthController.login("admin", "")

    def test_register_password_mismatch(self):
        """Mismatched passwords raise ValueError"""
        with pytest.raises(ValueError, match="Passwords do not match"):
            AuthController.register("newuser99", "pass1234", "different", "e@e.com")

    def test_register_short_username(self):
        """Username less than 3 chars raises ValueError"""
        with pytest.raises(ValueError, match="at least 3 characters"):
            AuthController.register("ab", "pass1234", "pass1234")

    def test_register_short_password(self):
        """Password less than 4 chars raises ValueError"""
        with pytest.raises(ValueError, match="at least 4 characters"):
            AuthController.register("validuser", "ab", "ab")

    def test_register_duplicate_username(self):
        """Registering existing username raises ValueError"""
        with pytest.raises(ValueError, match="already taken"):
            AuthController.register("admin", "newpass123", "newpass123")


# ══════════════════════════════════════════════
#  TASK CONTROLLER TESTS
# ══════════════════════════════════════════════

class TestTaskController:

    def test_add_task_returns_id(self, test_user):
        """Adding a task should return a valid integer ID"""
        cats = TaskController.get_categories(test_user.id)
        cat_id = cats[0].id if cats else None
        task_id = TaskController.add_task(
            test_user.id, "New Test Task", "desc",
            "High", "Pending", "2025-11-30", cat_id
        )
        assert isinstance(task_id, int)
        assert task_id > 0
        TaskController.remove_task(task_id)

    def test_add_task_empty_title_raises(self, test_user):
        """Empty title should raise ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            TaskController.add_task(test_user.id, "", "desc", "Low", "Pending", None, None)

    def test_add_task_short_title_raises(self, test_user):
        """Title shorter than 3 chars raises ValueError"""
        with pytest.raises(ValueError, match="at least 3 characters"):
            TaskController.add_task(test_user.id, "ab", "desc", "Low", "Pending", None, None)

    def test_add_task_invalid_priority(self, test_user):
        """Invalid priority raises ValueError"""
        with pytest.raises(ValueError, match="Invalid priority"):
            TaskController.add_task(
                test_user.id, "Good Title", "d", "Ultra", "Pending", None, None)

    def test_add_task_invalid_status(self, test_user):
        """Invalid status raises ValueError"""
        with pytest.raises(ValueError, match="Invalid status"):
            TaskController.add_task(
                test_user.id, "Good Title", "d", "Low", "Floating", None, None)

    def test_get_tasks_returns_list(self, test_user, sample_task_id):
        """get_tasks should return a list"""
        tasks = TaskController.get_tasks(test_user.id)
        assert isinstance(tasks, list)
        assert len(tasks) >= 1

    def test_get_tasks_filter_status(self, test_user, sample_task_id):
        """Filtering by status 'Pending' returns correct tasks"""
        tasks = TaskController.get_tasks(test_user.id, status_filter="Pending")
        for t in tasks:
            assert t.status == "Pending"

    def test_get_tasks_search(self, test_user, sample_task_id):
        """Search by keyword finds matching tasks"""
        tasks = TaskController.get_tasks(test_user.id, search="Fixture Test")
        assert any("Fixture Test" in t.title for t in tasks)

    def test_edit_task_updates_title(self, test_user, sample_task_id):
        """Editing task changes the title"""
        TaskController.edit_task(
            sample_task_id, "Updated Title Here", "new desc",
            "High", "In Progress", "2025-12-01", None
        )
        task = Task.get_by_id(sample_task_id)
        assert task.title == "Updated Title Here"
        assert task.status == "In Progress"

    def test_delete_task_removes_it(self, test_user):
        """Deleting a task removes it from DB"""
        cats = TaskController.get_categories(test_user.id)
        cat_id = cats[0].id if cats else None
        tid = TaskController.add_task(
            test_user.id, "Delete Me Task", "",
            "Low", "Pending", None, cat_id
        )
        TaskController.remove_task(tid)
        assert Task.get_by_id(tid) is None

    def test_dashboard_stats_structure(self, test_user):
        """Dashboard stats should have all required keys"""
        stats = TaskController.get_dashboard_stats(test_user.id)
        for key in ["Total", "Pending", "In Progress", "Completed", "Cancelled"]:
            assert key in stats
            assert isinstance(stats[key], int)

    def test_get_categories_returns_list(self, test_user):
        """get_categories returns a list (may be empty for new test user)"""
        cats = TaskController.get_categories(test_user.id)
        assert isinstance(cats, list)  # Must always return a list

    def test_add_category_success(self, test_user):
        """Adding a valid category should succeed"""
        result = TaskController.add_category("PyTest Cat", "#ff0000", test_user.id)
        assert result is True

    def test_add_category_empty_name(self, test_user):
        """Empty category name raises ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            TaskController.add_category("", "#ff0000", test_user.id)


# ══════════════════════════════════════════════
#  TASK MODEL TESTS
# ══════════════════════════════════════════════

class TestTaskModel:

    def test_task_to_dict_has_all_keys(self):
        """to_dict should return all expected keys"""
        t = Task(id=1, title="Sample", user_id=1)
        d = t.to_dict()
        for key in ["id", "title", "description", "priority",
                    "status", "due_date", "user_id"]:
            assert key in d

    def test_task_is_overdue_past_date(self):
        """Task with past due date and Pending status is overdue"""
        t = Task(id=1, title="T", due_date="2020-01-01", status="Pending", user_id=1)
        assert t.is_overdue() is True

    def test_task_is_overdue_completed(self):
        """Completed task is NOT overdue even with past due date"""
        t = Task(id=1, title="T", due_date="2020-01-01", status="Completed", user_id=1)
        assert t.is_overdue() is False

    def test_task_is_not_overdue_no_date(self):
        """Task with no due date is not overdue"""
        t = Task(id=1, title="T", due_date=None, status="Pending", user_id=1)
        assert t.is_overdue() is False

    def test_task_repr(self):
        """Task repr includes class name and id"""
        t = Task(id=42, title="Test", user_id=1)
        assert "Task" in repr(t)
        assert "42" in repr(t)

    def test_user_to_dict(self):
        """User to_dict returns correct fields"""
        u = User(id=1, username="ali", password="pass", email="a@b.com")
        d = u.to_dict()
        assert d["username"] == "ali"
        assert "password" not in d   # Password should be private!

    def test_user_password_encapsulation(self):
        """Setting a short password should raise ValueError"""
        u = User()
        with pytest.raises(ValueError):
            u.password = "abc"   # Too short

    def test_task_priorities_list(self):
        """Task should have exactly 4 priorities"""
        assert len(Task.PRIORITIES) == 4
        assert "Critical" in Task.PRIORITIES

    def test_task_statuses_list(self):
        """Task should have exactly 4 statuses"""
        assert len(Task.STATUSES) == 4
        assert "Completed" in Task.STATUSES
