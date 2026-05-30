"""
database.py - Database Layer for Task Management System
Handles all SQLite operations using OOP principles
"""

import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    """Base class for database connection management (OOP - Base Class)"""

    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'taskmanager.db')

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Open database connection"""
        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.row_factory = sqlite3.Row  # Return dict-like rows
        self.cursor = self.conn.cursor()
        return self

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def commit(self):
        """Commit transaction"""
        if self.conn:
            self.conn.commit()

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        self.disconnect()


class TaskManagerDB(DatabaseManager):
    """
    Extended DB class for Task Management System
    Inherits from DatabaseManager (OOP - Inheritance)
    """

    def initialize_tables(self):
        """Create tables if they don't exist"""
        with self as db:
            # Users table
            db.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Categories table
            db.cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    color TEXT DEFAULT '#3498db',
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

            # Tasks table
            db.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT DEFAULT 'Medium',
                    status TEXT DEFAULT 'Pending',
                    due_date TEXT,
                    category_id INTEGER,
                    user_id INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

            # Insert default admin user if not exists
            db.cursor.execute("""
                INSERT OR IGNORE INTO users (username, password, email)
                VALUES ('admin', 'admin123', 'admin@taskmanager.com')
            """)

            # Insert default categories
            default_cats = [
                ('Work', '#e74c3c', 1),
                ('Personal', '#2ecc71', 1),
                ('Study', '#9b59b6', 1),
                ('Health', '#f39c12', 1),
            ]
            db.cursor.executemany("""
                INSERT OR IGNORE INTO categories (name, color, user_id)
                VALUES (?, ?, ?)
            """, default_cats)


# Initialize DB on import
_db = TaskManagerDB()
_db.initialize_tables()
