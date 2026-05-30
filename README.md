# ✔ TaskFlow — Task Management System

> A full-featured Task Management System built with Python, Tkinter GUI, SQLite database, and OOP principles.

---

## 👥 Group Members

| Name | Role |
|------|------|
| Member 1 | Models & Database Layer |
| Member 2 | Controllers & Business Logic |
| Member 3 | GUI / Views & Unit Tests |

---

## 📌 Project Overview

TaskFlow is a desktop Task Management System that helps users create, manage, and track tasks with priorities, categories, due dates, and status updates. Built following MVC (Model-View-Controller) architecture.

---

## 🛠️ Technologies Used

| Tool / Technology | Purpose |
|---|---|
| Python 3.x | Primary programming language |
| Tkinter | GUI framework |
| SQLite3 | Local database |
| PyTest | Unit testing |
| Git & GitHub | Version control |
| VS Code | IDE |

---

## 📁 Project Structure

```
task_manager/
│
├── app.py                      # Main entry point (GUI)
│
├── models/
│   ├── __init__.py
│   ├── database.py             # DatabaseManager base class + SQLite setup
│   └── models.py               # Task, User, Category models (OOP)
│
├── controllers/
│   ├── __init__.py
│   └── task_controller.py      # Business logic (AuthController, TaskController)
│
├── tests/
│   ├── __init__.py
│   └── test_task_manager.py    # 25+ PyTest unit tests
│
├── requirements.txt
└── README.md
```

---

## ⚙️ OOP Concepts Applied

| Concept | Where Used |
|---|---|
| **Classes & Objects** | `Task`, `User`, `Category`, `DatabaseManager` |
| **Inheritance** | `TaskManagerDB` inherits `DatabaseManager`; `Task`, `User`, `Category` inherit `BaseModel` |
| **Polymorphism** | `to_dict()` overridden in each model subclass |
| **Encapsulation** | `User._password` with property getter/setter |
| **MVC Pattern** | Models / Controllers / Views separated |

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install pytest
```

### 2. Run the Application
```bash
cd task_manager
python app.py
```

### 3. Default Login
```
Username: admin
Password: admin123
```

### 4. Run Unit Tests
```bash
cd task_manager
pytest tests/ -v
```

---

## ✅ Features

- 🔐 **User Authentication** — Login / Register system
- ➕ **Task CRUD** — Create, Read, Update, Delete tasks
- 🏷️ **Categories** — Organize tasks by custom categories
- 🎯 **Priority Levels** — Low, Medium, High, Critical
- 📊 **Status Tracking** — Pending, In Progress, Completed, Cancelled
- 🔍 **Search & Filter** — Search by title, filter by status/priority
- 📈 **Dashboard Stats** — Live task count by status
- 🌑 **Dark Theme UI** — Professional dark mode interface

---

## 🧪 Testing

- **Framework**: PyTest
- **Test File**: `tests/test_task_manager.py`
- **Tests Count**: 25+ unit tests
- **Coverage**:
  - Authentication (login/register validation)
  - Task CRUD operations
  - Input validation & error handling
  - Model methods (`to_dict`, `is_overdue`, `repr`)
  - Edge cases (empty fields, invalid values)

---

## 🗃️ Database Schema

```sql
users (id, username, password, email, created_at)
categories (id, name, color, user_id)
tasks (id, title, description, priority, status, due_date, category_id, user_id, created_at, updated_at)
```

---

## 📝 Git Commit Guidelines

```
feat: add task creation form
fix: resolve login validation bug
test: add unit tests for TaskController
refactor: extract business logic to controller
docs: update README with setup instructions
```

---

## 🔧 Debugging & Error Handling

- All user inputs validated in `TaskController.validate_task()`
- Custom `ValueError` exceptions with descriptive messages
- `try/except` blocks in all DB operations
- SQLite foreign key constraints enforced

---

## 📦 Deployment

- **Local**: Run `python app.py`
- **GitHub**: Push to repository with commit history
- **GitHub Pages**: N/A (Desktop app — distribute as `.py` or package with PyInstaller)

---

## 👤 Individual Contributions

Each group member should add their personal contribution section in their **Individual Report**.

---

*Final Lab Project — Software Construction and Development Lab*
