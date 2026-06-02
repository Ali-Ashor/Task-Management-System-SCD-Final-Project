# 🚀 TaskFlow — Smart Task Management System

<div align="center">

### Organize • Prioritize • Track • Achieve

A modern desktop-based Task Management System developed using **Python**, **Tkinter**, **SQLite3**, and the **MVC (Model-View-Controller)** architecture.

<br>

<br>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-6A5ACD?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)
![MVC](https://img.shields.io/badge/Architecture-MVC-FF6B6B?style=for-the-badge)
![PyTest](https://img.shields.io/badge/PyTest-32_Tests_Passed-success?style=for-the-badge\&logo=pytest)

</div>

---

# 📖 Project Overview

TaskFlow is a desktop-based Task Management System designed to help users efficiently organize, monitor, and manage their daily activities. The application provides a centralized platform where users can create tasks, assign priorities, categorize work, track progress, and monitor deadlines through a modern dark-themed graphical interface.

The system supports multiple user accounts, allowing each user to maintain a personal workspace. Users can create custom categories, assign due dates, update task statuses, and analyze productivity through real-time dashboard statistics.

TaskFlow is developed using Python, Tkinter, and SQLite3 while following the MVC (Model-View-Controller) architectural pattern. This approach ensures a clear separation between the user interface, business logic, and database layer, resulting in a maintainable and scalable application.

---

# 🎯 Problem Statement

Managing tasks manually often results in missed deadlines, poor prioritization, and reduced productivity. Many available solutions are either too complex or require continuous internet connectivity.

TaskFlow addresses these challenges by providing a lightweight desktop application that enables users to efficiently manage tasks, organize workloads, and track progress through an intuitive interface.

---

# 🎯 Project Objectives

* Develop a user-friendly task management application.
* Implement secure user authentication.
* Provide complete task CRUD functionality.
* Allow task categorization and prioritization.
* Enable deadline and overdue task tracking.
* Demonstrate Object-Oriented Programming concepts.
* Apply MVC architecture principles.
* Perform automated testing using PyTest.
* Maintain data persistence through SQLite.

---

# ✨ Key Features

## 🔐 User Authentication

* User Registration
* Secure Login System
* Individual User Workspaces
* Session-Based Access

## 📋 Task Management

* Create Tasks
* View Tasks
* Update Tasks
* Delete Tasks
* Task Validation

## 🏷️ Categories

* Create Custom Categories
* Organize Tasks Efficiently
* User-Specific Categories
* Color-Based Categorization

## 🎯 Priority Management

* Low
* Medium
* High
* Critical

## 📊 Status Tracking

* Pending
* In Progress
* Completed
* Cancelled

## 📅 Due Date Management

* Assign Deadlines
* Automatic Overdue Detection
* Task Scheduling

## 🔍 Search & Filtering

* Search by Task Title
* Filter by Status
* Filter by Priority
* Dynamic Results

## 📈 Dashboard Analytics

* Total Tasks Count
* Pending Tasks Count
* In Progress Tasks Count
* Completed Tasks Count
* Real-Time Statistics

## 🌙 Modern Dark Theme UI

* Professional Interface
* Clean Layout
* Improved User Experience

---

# 📸 Application Screenshots

## 🔐 Login Window

<p align="center">
<img src="screenshots/login.png" width="500">
</p>

The login window allows registered users to securely access their personal workspace. New users can register through the integrated account creation system.

---

## 📊 Dashboard

<p align="center">
<img width="1364" height="719" alt="image" src="https://github.com/user-attachments/assets/ce160654-67ac-4267-b861-f0269c1b59d2" />

</p>

The dashboard provides a complete overview of tasks, statistics, filters, and task management operations in a single interface.

---

# 🏗 MVC Architecture

```text
                ┌─────────────────┐
                │      View       │
                │   Tkinter GUI   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Controller    │
                │ Business Logic  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │      Model      │
                │ SQLite Database │
                └─────────────────┘
```

### Architecture Description

**Model Layer**

* Handles database operations.
* Stores and retrieves application data.
* Represents Task, User, and Category entities.

**Controller Layer**

* Processes user requests.
* Validates input data.
* Implements business rules.

**View Layer**

* Provides the graphical user interface.
* Displays information to users.
* Captures user interactions.

---

# 🧠 Object-Oriented Programming Concepts

| Concept           | Implementation                                       |
| ----------------- | ---------------------------------------------------- |
| Classes & Objects | Task, User, Category, DatabaseManager                |
| Inheritance       | Task, User, Category inherit BaseModel               |
| Polymorphism      | to_dict() overridden in subclasses                   |
| Encapsulation     | Password protected through property methods          |
| Abstraction       | Database operations separated into dedicated classes |
| MVC Pattern       | Models, Views, and Controllers separated             |

---

# 🗃️ Database Design

## Users Table

```sql
users (
    id,
    username,
    password,
    email,
    created_at
)
```

## Categories Table

```sql
categories (
    id,
    name,
    color,
    user_id
)
```

## Tasks Table

```sql
tasks (
    id,
    title,
    description,
    priority,
    status,
    due_date,
    category_id,
    user_id,
    created_at,
    updated_at
)
```

---

# 📂 Project Structure

```bash
task_manager/
│
├── app.py
│
├── models/
│   ├── database.py
│   └── models.py
│
├── controllers/
│   └── task_controller.py
│
├── tests/
│   └── test_task_manager.py
│
├── taskmanager.db
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Technology | Purpose                 |
| ---------- | ----------------------- |
| Python 3.x | Application Development |
| Tkinter    | GUI Development         |
| SQLite3    | Data Storage            |
| PyTest     | Unit Testing            |
| Git        | Version Control         |
| GitHub     | Collaboration           |
| VS Code    | Development Environment |

---

# 🚀 Installation Guide

## Clone Repository

```bash
git clone https://github.com/your-username/taskflow.git
```

## Move into Project Folder

```bash
cd taskflow
```

## Install Dependencies

```bash
pip install pytest
```

## Run Application

```bash
python app.py
```

The SQLite database is automatically created during the first launch.

---

# 🔑 Default Credentials

```text
Username: admin
Password: admin123
```

---

# 🧪 Testing

The project contains a comprehensive test suite developed using PyTest.

| Test Class      | Coverage             | Tests |
| --------------- | -------------------- | ----- |
| Authentication  | Login & Registration | 9     |
| Task Controller | CRUD Operations      | 13    |
| Models          | Validation & Logic   | 10    |
| Total           |                      | 32 ✅  |

### Test Execution

```bash
pytest tests/ -v
```

---

# ⚠️ Error Handling

* Input validation before database operations.
* Custom ValueError exceptions.
* Database exception handling using try/except blocks.
* SQLite foreign key enforcement.
* GUI error dialogs using messagebox.

---

# 👥 Team Contributions

## Shujaat Ali (41957)

### Models & Database Layer

* Designed database schema.
* Implemented DatabaseManager.
* Developed BaseModel hierarchy.
* Created CRUD operations.
* Applied inheritance and polymorphism.

---

## Muhammad Abbas (42490)

### Controllers & Business Logic

* Developed AuthController.
* Developed TaskController.
* Implemented validation rules.
* Applied encapsulation.
* Implemented business logic.

---

## Muhammad Bilal (42029)

### GUI & Testing

* Developed Tkinter GUI.
* Implemented dashboard system.
* Created search and filtering interface.
* Wrote 32 PyTest test cases.
* Conducted integration testing.

---

# 🚀 Future Enhancements

* Email reminders
* PDF report generation
* Excel export functionality
* Calendar integration
* Cloud synchronization
* Team collaboration features
* Mobile application support
* Dark/Light theme switching

---

# 📚 References

* Python Documentation
* Tkinter Documentation
* SQLite3 Documentation
* PyTest Documentation
* Git Documentation
* Real Python OOP Guide

---

<div align="center">

## ⭐ TaskFlow — Manage Tasks Smarter

Software Construction & Development Lab Project

Federal Urdu University of Arts, Science & Technology (FUUAST)

BS Software Engineering — Semester 5

Spring 2026

Made with Python, Tkinter, SQLite3 & MVC Architecture

</div>
