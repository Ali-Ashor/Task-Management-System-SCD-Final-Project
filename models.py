"""
models.py - OOP Models for Task Management System
Demonstrates: Classes, Inheritance, Polymorphism, Encapsulation
"""

from datetime import datetime
from models.database import TaskManagerDB


# ─────────────────────────────────────────────
#  BASE MODEL (Parent Class)
# ─────────────────────────────────────────────
class BaseModel:
    """Abstract base model with common CRUD interface (OOP - Base Class)"""

    TABLE = None

    def __repr__(self):
        return f"<{self.__class__.__name__} id={getattr(self, 'id', None)}>"

    def to_dict(self):
        """Polymorphic method - overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement to_dict()")


# ─────────────────────────────────────────────
#  USER MODEL
# ─────────────────────────────────────────────
class User(BaseModel):
    """User model - inherits from BaseModel (OOP - Inheritance)"""

    TABLE = "users"

    def __init__(self, id=None, username="", password="", email="", created_at=None):
        self.id = id
        self.username = username
        self._password = password       # Encapsulation: private attribute
        self.email = email
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Property (Encapsulation)
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if len(value) < 4:
            raise ValueError("Password must be at least 4 characters")
        self._password = value

    def to_dict(self):
        """Polymorphic override"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }

    # ── Static / Class Methods ──────────────────

    @staticmethod
    def authenticate(username: str, password: str):
        """Check credentials and return User object or None"""
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )
            row = d.cursor.fetchone()
        if row:
            return User(id=row["id"], username=row["username"],
                        password=row["password"], email=row["email"] or "",
                        created_at=row["created_at"])
        return None

    @staticmethod
    def create(username: str, password: str, email: str = ""):
        """Register a new user; returns True on success"""
        try:
            db = TaskManagerDB()
            with db as d:
                d.cursor.execute(
                    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                    (username, password, email)
                )
            return True
        except Exception:
            return False

    @staticmethod
    def exists(username: str) -> bool:
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            return d.cursor.fetchone() is not None


# ─────────────────────────────────────────────
#  CATEGORY MODEL
# ─────────────────────────────────────────────
class Category(BaseModel):
    """Category model"""

    TABLE = "categories"

    def __init__(self, id=None, name="", color="#3498db", user_id=None):
        self.id = id
        self.name = name
        self.color = color
        self.user_id = user_id

    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "color": self.color, "user_id": self.user_id}

    @staticmethod
    def get_all(user_id: int):
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute(
                "SELECT * FROM categories WHERE user_id=? OR user_id IS NULL", (user_id,))
            rows = d.cursor.fetchall()
        return [Category(id=r["id"], name=r["name"],
                         color=r["color"], user_id=r["user_id"]) for r in rows]

    @staticmethod
    def create(name: str, color: str, user_id: int):
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute(
                "INSERT INTO categories (name, color, user_id) VALUES (?, ?, ?)",
                (name, color, user_id)
            )
        return True


# ─────────────────────────────────────────────
#  TASK MODEL
# ─────────────────────────────────────────────
class Task(BaseModel):
    """
    Task model - Inherits BaseModel (OOP - Inheritance)
    Demonstrates full CRUD operations
    """

    TABLE = "tasks"
    PRIORITIES = ["Low", "Medium", "High", "Critical"]
    STATUSES = ["Pending", "In Progress", "Completed", "Cancelled"]

    def __init__(self, id=None, title="", description="", priority="Medium",
                 status="Pending", due_date=None, category_id=None,
                 user_id=None, created_at=None, updated_at=None,
                 category_name=None):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.category_id = category_id
        self.category_name = category_name or "General"
        self.user_id = user_id
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or self.created_at

    def to_dict(self):
        """Polymorphic override"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "user_id": self.user_id,
            "created_at": self.created_at,
        }

    def is_overdue(self) -> bool:
        """Check if task is past due date"""
        if not self.due_date:
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
            return due < datetime.now() and self.status not in ("Completed", "Cancelled")
        except ValueError:
            return False

    # ── CRUD Operations ─────────────────────────

    @staticmethod
    def get_all(user_id: int, status_filter: str = None,
                priority_filter: str = None, search: str = None):
        """Fetch tasks for a user with optional filters"""
        db = TaskManagerDB()
        query = """
            SELECT t.*, c.name as category_name
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ?
        """
        params = [user_id]
        if status_filter and status_filter != "All":
            query += " AND t.status = ?"
            params.append(status_filter)
        if priority_filter and priority_filter != "All":
            query += " AND t.priority = ?"
            params.append(priority_filter)
        if search:
            query += " AND (t.title LIKE ? OR t.description LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        query += " ORDER BY t.created_at DESC"

        with db as d:
            d.cursor.execute(query, params)
            rows = d.cursor.fetchall()
        return [Task._from_row(r) for r in rows]

    @staticmethod
    def get_by_id(task_id: int):
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute("""
                SELECT t.*, c.name as category_name
                FROM tasks t LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.id = ?
            """, (task_id,))
            row = d.cursor.fetchone()
        return Task._from_row(row) if row else None

    @staticmethod
    def create(title: str, description: str, priority: str, status: str,
               due_date: str, category_id: int, user_id: int):
        """Insert a new task"""
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute("""
                INSERT INTO tasks (title, description, priority, status,
                                   due_date, category_id, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, description, priority, status, due_date, category_id, user_id))
            return d.cursor.lastrowid

    @staticmethod
    def update(task_id: int, title: str, description: str, priority: str,
               status: str, due_date: str, category_id: int):
        """Update existing task"""
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute("""
                UPDATE tasks
                SET title=?, description=?, priority=?, status=?,
                    due_date=?, category_id=?, updated_at=?
                WHERE id=?
            """, (title, description, priority, status, due_date,
                  category_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_id))
        return True

    @staticmethod
    def delete(task_id: int):
        """Delete a task"""
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        return True

    @staticmethod
    def get_stats(user_id: int) -> dict:
        """Return task statistics for dashboard"""
        db = TaskManagerDB()
        with db as d:
            d.cursor.execute(
                "SELECT status, COUNT(*) as cnt FROM tasks WHERE user_id=? GROUP BY status",
                (user_id,))
            rows = d.cursor.fetchall()
        stats = {"Total": 0, "Pending": 0, "In Progress": 0,
                 "Completed": 0, "Cancelled": 0}
        for r in rows:
            stats[r["status"]] = r["cnt"]
            stats["Total"] += r["cnt"]
        return stats

    @staticmethod
    def _from_row(row) -> "Task":
        return Task(
            id=row["id"], title=row["title"], description=row["description"] or "",
            priority=row["priority"], status=row["status"],
            due_date=row["due_date"], category_id=row["category_id"],
            user_id=row["user_id"], created_at=row["created_at"],
            updated_at=row["updated_at"],
            category_name=row["category_name"] if "category_name" in row.keys() else "General"
        )
