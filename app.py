"""
app.py - Main GUI Application (Tkinter)
Task Management System - Full UI with Login, Dashboard, CRUD
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.task_controller import AuthController, TaskController
from models.models import Task


# ═══════════════════════════════════════════════
#  THEME & COLORS
# ═══════════════════════════════════════════════
COLORS = {
    "bg":           "#0f1117",
    "surface":      "#1a1d27",
    "card":         "#22263a",
    "accent":       "#6c63ff",
    "accent2":      "#ff6584",
    "success":      "#43e97b",
    "warning":      "#f9ca24",
    "danger":       "#ff4757",
    "info":         "#45aaf2",
    "text":         "#e8eaf6",
    "text_muted":   "#7f8b9e",
    "border":       "#2d3246",
}

PRIORITY_COLORS = {
    "Low":      "#43e97b",
    "Medium":   "#f9ca24",
    "High":     "#ff6b35",
    "Critical": "#ff4757",
}

STATUS_COLORS = {
    "Pending":     "#7f8b9e",
    "In Progress": "#45aaf2",
    "Completed":   "#43e97b",
    "Cancelled":   "#ff4757",
}


def styled_button(parent, text, command, bg=None, fg=None,
                  width=12, font_size=10, **kw):
    bg = bg or COLORS["accent"]
    fg = fg or COLORS["text"]
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, relief="flat", bd=0,
        font=("Segoe UI", font_size, "bold"),
        activebackground=COLORS["accent2"],
        activeforeground=COLORS["text"],
        cursor="hand2", width=width,
        padx=8, pady=6, **kw
    )
    return btn


def styled_entry(parent, textvariable=None, show=None, width=30):
    e = tk.Entry(
        parent,
        textvariable=textvariable,
        bg=COLORS["card"], fg=COLORS["text"],
        insertbackground=COLORS["text"],
        relief="flat", bd=0,
        font=("Segoe UI", 10),
        show=show or "",
        width=width,
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["accent"]
    )
    return e


# ═══════════════════════════════════════════════
#  LOGIN WINDOW
# ═══════════════════════════════════════════════
class LoginWindow(tk.Toplevel):

    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.title("Task Manager — Login")
        self.geometry("420x520")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self.grab_set()
        self._build_ui()
        self.lift()

    def _build_ui(self):
        # Header
        tk.Label(self, text="✔ TaskFlow", font=("Segoe UI", 26, "bold"),
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(40, 4))
        tk.Label(self, text="Sign in to your workspace",
                 font=("Segoe UI", 10), bg=COLORS["bg"],
                 fg=COLORS["text_muted"]).pack(pady=(0, 30))

        card = tk.Frame(self, bg=COLORS["surface"], bd=0)
        card.pack(padx=40, fill="x")

        # Username
        tk.Label(card, text="Username", bg=COLORS["surface"],
                 fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(20, 2))
        self.username_var = tk.StringVar()
        styled_entry(card, self.username_var, width=32).pack(padx=20, pady=(0, 12), fill="x")

        # Password
        tk.Label(card, text="Password", bg=COLORS["surface"],
                 fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(0, 2))
        self.password_var = tk.StringVar()
        styled_entry(card, self.password_var, show="●", width=32).pack(padx=20, pady=(0, 20), fill="x")

        # Login button
        styled_button(card, "Sign In", self._login,
                      width=34, font_size=11).pack(padx=20, pady=(0, 16), fill="x")

        # Register link
        tk.Label(card, text="Don't have an account?",
                 bg=COLORS["surface"], fg=COLORS["text_muted"],
                 font=("Segoe UI", 9)).pack()
        styled_button(card, "Create Account", self._open_register,
                      bg=COLORS["card"], width=34).pack(padx=20, pady=(6, 20), fill="x")

        tk.Label(self, text="Default: admin / admin123",
                 bg=COLORS["bg"], fg=COLORS["text_muted"],
                 font=("Segoe UI", 8)).pack(pady=12)

        self.bind("<Return>", lambda e: self._login())

    def _login(self):
        try:
            user = AuthController.login(self.username_var.get(), self.password_var.get())
            self.on_login_success(user)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e), parent=self)

    def _open_register(self):
        RegisterWindow(self)


# ═══════════════════════════════════════════════
#  REGISTER WINDOW
# ═══════════════════════════════════════════════
class RegisterWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title("Create Account")
        self.geometry("400x480")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self.grab_set()
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Create Account", font=("Segoe UI", 20, "bold"),
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(30, 20))

        card = tk.Frame(self, bg=COLORS["surface"])
        card.pack(padx=30, fill="x")

        fields = [
            ("Username *", "username_var", False),
            ("Password *", "password_var", True),
            ("Confirm Password *", "confirm_var", True),
            ("Email (optional)", "email_var", False),
        ]

        for label, var_name, hide in fields:
            tk.Label(card, text=label, bg=COLORS["surface"],
                     fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(12, 2))
            v = tk.StringVar()
            setattr(self, var_name, v)
            styled_entry(card, v, show="●" if hide else None, width=32).pack(padx=20, fill="x")

        styled_button(card, "Register", self._register,
                      bg=COLORS["success"], fg="#000",
                      width=34, font_size=11).pack(padx=20, pady=20, fill="x")

    def _register(self):
        try:
            AuthController.register(
                self.username_var.get(), self.password_var.get(),
                self.confirm_var.get(), self.email_var.get()
            )
            messagebox.showinfo("Success", "Account created! You can now login.", parent=self)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)


# ═══════════════════════════════════════════════
#  TASK FORM (Add / Edit)
# ═══════════════════════════════════════════════
class TaskFormWindow(tk.Toplevel):

    def __init__(self, master, user, categories, task=None, on_save=None):
        super().__init__(master)
        self.user = user
        self.categories = categories
        self.task = task
        self.on_save = on_save
        self.title("Edit Task" if task else "New Task")
        self.geometry("480x560")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self.grab_set()
        self._build_ui()
        if task:
            self._populate(task)

    def _build_ui(self):
        tk.Label(self, text="📝 " + ("Edit Task" if self.task else "New Task"),
                 font=("Segoe UI", 16, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=(20, 16))

        card = tk.Frame(self, bg=COLORS["surface"])
        card.pack(padx=24, fill="both", expand=True)

        def lbl(text):
            tk.Label(card, text=text, bg=COLORS["surface"],
                     fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(12, 2))

        # Title
        lbl("Task Title *")
        self.title_var = tk.StringVar()
        styled_entry(card, self.title_var, width=44).pack(padx=20, fill="x")

        # Description
        lbl("Description")
        self.desc_text = tk.Text(card, bg=COLORS["card"], fg=COLORS["text"],
                                  insertbackground=COLORS["text"],
                                  relief="flat", height=3,
                                  font=("Segoe UI", 10),
                                  highlightthickness=1,
                                  highlightbackground=COLORS["border"])
        self.desc_text.pack(padx=20, fill="x")

        row = tk.Frame(card, bg=COLORS["surface"])
        row.pack(padx=20, fill="x", pady=(8, 0))

        # Priority
        col1 = tk.Frame(row, bg=COLORS["surface"])
        col1.pack(side="left", expand=True, fill="x", padx=(0, 8))
        tk.Label(col1, text="Priority", bg=COLORS["surface"],
                 fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(anchor="w")
        self.priority_var = tk.StringVar(value="Medium")
        ttk.Combobox(col1, textvariable=self.priority_var,
                     values=Task.PRIORITIES, state="readonly",
                     width=14).pack(fill="x")

        # Status
        col2 = tk.Frame(row, bg=COLORS["surface"])
        col2.pack(side="left", expand=True, fill="x")
        tk.Label(col2, text="Status", bg=COLORS["surface"],
                 fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(anchor="w")
        self.status_var = tk.StringVar(value="Pending")
        ttk.Combobox(col2, textvariable=self.status_var,
                     values=Task.STATUSES, state="readonly",
                     width=14).pack(fill="x")

        # Due Date
        lbl("Due Date (YYYY-MM-DD)")
        self.due_var = tk.StringVar()
        styled_entry(card, self.due_var, width=44).pack(padx=20, fill="x")

        # Category
        lbl("Category")
        self.cat_var = tk.StringVar()
        cat_names = [c.name for c in self.categories]
        self.cat_combo = ttk.Combobox(card, textvariable=self.cat_var,
                                       values=cat_names, state="readonly", width=42)
        self.cat_combo.pack(padx=20, fill="x")
        if cat_names:
            self.cat_combo.current(0)

        # Buttons
        btn_row = tk.Frame(card, bg=COLORS["surface"])
        btn_row.pack(padx=20, pady=20, fill="x")
        styled_button(btn_row, "💾 Save", self._save,
                      bg=COLORS["accent"], width=18).pack(side="left", padx=(0, 8))
        styled_button(btn_row, "✕ Cancel", self.destroy,
                      bg=COLORS["card"], width=12).pack(side="left")

    def _populate(self, task):
        self.title_var.set(task.title)
        self.desc_text.insert("1.0", task.description)
        self.priority_var.set(task.priority)
        self.status_var.set(task.status)
        self.due_var.set(task.due_date or "")
        if task.category_name:
            self.cat_var.set(task.category_name)

    def _save(self):
        try:
            cat_name = self.cat_var.get()
            cat_id = next((c.id for c in self.categories if c.name == cat_name), None)
            desc = self.desc_text.get("1.0", "end-1c")
            due = self.due_var.get().strip() or None

            if self.task:
                TaskController.edit_task(
                    self.task.id, self.title_var.get(), desc,
                    self.priority_var.get(), self.status_var.get(),
                    due, cat_id
                )
                messagebox.showinfo("Saved", "Task updated successfully!", parent=self)
            else:
                TaskController.add_task(
                    self.user.id, self.title_var.get(), desc,
                    self.priority_var.get(), self.status_var.get(),
                    due, cat_id
                )
                messagebox.showinfo("Saved", "Task created!", parent=self)

            if self.on_save:
                self.on_save()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)


# ═══════════════════════════════════════════════
#  MAIN DASHBOARD
# ═══════════════════════════════════════════════
class DashboardWindow(tk.Frame):

    def __init__(self, master, user):
        super().__init__(master, bg=COLORS["bg"])
        self.user = user
        self.pack(fill="both", expand=True)
        self._search_var = tk.StringVar()
        self._status_filter = tk.StringVar(value="All")
        self._priority_filter = tk.StringVar(value="All")
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # ── Sidebar ─────────────────────────
        sidebar = tk.Frame(self, bg=COLORS["surface"], width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="✔ TaskFlow",
                 font=("Segoe UI", 16, "bold"),
                 bg=COLORS["surface"], fg=COLORS["accent"]).pack(pady=(24, 4))
        tk.Label(sidebar, text=f"👤 {self.user.username}",
                 font=("Segoe UI", 9),
                 bg=COLORS["surface"], fg=COLORS["text_muted"]).pack(pady=(0, 20))

        # Stats labels
        self.stat_frames = {}
        stats_info = [
            ("Total", COLORS["text"]),
            ("Pending", STATUS_COLORS["Pending"]),
            ("In Progress", STATUS_COLORS["In Progress"]),
            ("Completed", STATUS_COLORS["Completed"]),
        ]
        for key, color in stats_info:
            f = tk.Frame(sidebar, bg=COLORS["card"], pady=8)
            f.pack(padx=12, pady=4, fill="x")
            tk.Label(f, text=key, font=("Segoe UI", 8),
                     bg=COLORS["card"], fg=COLORS["text_muted"]).pack()
            lbl = tk.Label(f, text="0", font=("Segoe UI", 20, "bold"),
                           bg=COLORS["card"], fg=color)
            lbl.pack()
            self.stat_frames[key] = lbl

        # Sidebar buttons
        btns = [
            ("➕ New Task", self._new_task, COLORS["accent"]),
            ("📁 Categories", self._manage_categories, COLORS["card"]),
            ("🚪 Logout", self._logout, COLORS["danger"]),
        ]
        for text, cmd, bg in btns:
            styled_button(sidebar, text, cmd, bg=bg, width=20).pack(
                padx=12, pady=4, fill="x")

        # ── Main content ─────────────────────
        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(side="left", fill="both", expand=True)

        # Toolbar
        toolbar = tk.Frame(main, bg=COLORS["surface"], pady=8)
        toolbar.pack(fill="x", padx=0, pady=0)

        # Search
        tk.Label(toolbar, text="🔍", bg=COLORS["surface"],
                 fg=COLORS["text_muted"], font=("Segoe UI", 12)).pack(side="left", padx=(16, 4))
        styled_entry(toolbar, self._search_var, width=24).pack(side="left", padx=(0, 16))
        styled_button(toolbar, "Search", self.refresh,
                      bg=COLORS["accent"], width=8).pack(side="left")

        # Filters
        tk.Label(toolbar, text="Status:", bg=COLORS["surface"],
                 fg=COLORS["text_muted"]).pack(side="left", padx=(20, 4))
        ttk.Combobox(toolbar, textvariable=self._status_filter,
                     values=["All"] + Task.STATUSES,
                     state="readonly", width=12).pack(side="left")

        tk.Label(toolbar, text="Priority:", bg=COLORS["surface"],
                 fg=COLORS["text_muted"]).pack(side="left", padx=(12, 4))
        ttk.Combobox(toolbar, textvariable=self._priority_filter,
                     values=["All"] + Task.PRIORITIES,
                     state="readonly", width=10).pack(side="left")

        styled_button(toolbar, "Clear", self._clear_filters,
                      bg=COLORS["card"], width=6).pack(side="left", padx=8)

        # Task list
        list_frame = tk.Frame(main, bg=COLORS["bg"])
        list_frame.pack(fill="both", expand=True, padx=16, pady=12)

        # Treeview style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background=COLORS["card"],
                         foreground=COLORS["text"],
                         rowheight=36,
                         fieldbackground=COLORS["card"],
                         borderwidth=0,
                         font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                         background=COLORS["surface"],
                         foreground=COLORS["text"],
                         font=("Segoe UI", 10, "bold"),
                         relief="flat")
        style.map("Treeview", background=[("selected", COLORS["accent"])])

        cols = ("Title", "Priority", "Status", "Category", "Due Date")
        self.tree = ttk.Treeview(list_frame, columns=cols,
                                  show="headings", selectmode="browse")
        widths = [280, 90, 110, 120, 110]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="w")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                   command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        action_bar = tk.Frame(main, bg=COLORS["bg"])
        action_bar.pack(fill="x", padx=16, pady=(0, 12))
        styled_button(action_bar, "✏️ Edit", self._edit_task,
                      bg=COLORS["info"], width=10).pack(side="left", padx=(0, 8))
        styled_button(action_bar, "🗑️ Delete", self._delete_task,
                      bg=COLORS["danger"], width=10).pack(side="left", padx=(0, 8))
        styled_button(action_bar, "✅ Complete", self._mark_complete,
                      bg=COLORS["success"], fg="#000", width=12).pack(side="left")

        # Status bar
        self.status_bar = tk.Label(main, text="Ready",
                                    bg=COLORS["surface"], fg=COLORS["text_muted"],
                                    font=("Segoe UI", 8), anchor="w")
        self.status_bar.pack(fill="x", padx=0, pady=0)

        # Store reference to categories
        self._categories = []

    # ── Data Operations ──────────────────────────

    def refresh(self, *_):
        """Reload tasks from DB and update UI"""
        self._categories = TaskController.get_categories(self.user.id)
        tasks = TaskController.get_tasks(
            self.user.id,
            status_filter=self._status_filter.get(),
            priority_filter=self._priority_filter.get(),
            search=self._search_var.get().strip() or None
        )

        self.tree.delete(*self.tree.get_children())
        for t in tasks:
            tag = t.status.replace(" ", "_")
            self.tree.insert("", "end", iid=str(t.id),
                              values=(t.title, t.priority, t.status,
                                      t.category_name, t.due_date or "—"),
                              tags=(tag,))
        for status, color in STATUS_COLORS.items():
            self.tree.tag_configure(status.replace(" ", "_"), foreground=color)

        # Update stats
        stats = TaskController.get_dashboard_stats(self.user.id)
        for key in self.stat_frames:
            self.stat_frames[key].config(text=str(stats.get(key, 0)))

        count = len(tasks)
        self.status_bar.config(text=f"  {count} task(s) found")

    def _get_selected_task_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return None
        return int(sel[0])

    def _new_task(self):
        TaskFormWindow(self.master, self.user,
                       self._categories, on_save=self.refresh)

    def _edit_task(self):
        tid = self._get_selected_task_id()
        if not tid:
            return
        from models.models import Task as TM
        task = TM.get_by_id(tid)
        if task:
            TaskFormWindow(self.master, self.user,
                           self._categories, task=task, on_save=self.refresh)

    def _delete_task(self):
        tid = self._get_selected_task_id()
        if not tid:
            return
        if messagebox.askyesno("Confirm Delete",
                                "Are you sure you want to delete this task?"):
            TaskController.remove_task(tid)
            self.refresh()
            self.status_bar.config(text="  Task deleted.")

    def _mark_complete(self):
        tid = self._get_selected_task_id()
        if not tid:
            return
        from models.models import Task as TM
        task = TM.get_by_id(tid)
        if task:
            TaskController.edit_task(
                task.id, task.title, task.description,
                task.priority, "Completed",
                task.due_date, task.category_id
            )
            self.refresh()
            self.status_bar.config(text="  Task marked as Completed ✓")

    def _manage_categories(self):
        CategoryWindow(self.master, self.user, on_save=self.refresh)

    def _clear_filters(self):
        self._search_var.set("")
        self._status_filter.set("All")
        self._priority_filter.set("All")
        self.refresh()

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.pack_forget()
            self.master.show_login()


# ═══════════════════════════════════════════════
#  CATEGORY MANAGER
# ═══════════════════════════════════════════════
class CategoryWindow(tk.Toplevel):

    COLORS_OPTIONS = ["#e74c3c", "#2ecc71", "#3498db", "#9b59b6",
                      "#f39c12", "#1abc9c", "#e67e22", "#6c63ff"]

    def __init__(self, master, user, on_save=None):
        super().__init__(master)
        self.user = user
        self.on_save = on_save
        self.title("Manage Categories")
        self.geometry("360x420")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self.grab_set()
        self._build_ui()
        self._load()

    def _build_ui(self):
        tk.Label(self, text="📁 Categories",
                 font=("Segoe UI", 14, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=16)

        card = tk.Frame(self, bg=COLORS["surface"])
        card.pack(padx=20, fill="both", expand=True)

        self.listbox = tk.Listbox(card, bg=COLORS["card"], fg=COLORS["text"],
                                   font=("Segoe UI", 11), relief="flat",
                                   selectbackground=COLORS["accent"],
                                   height=8)
        self.listbox.pack(padx=16, pady=16, fill="both", expand=True)

        tk.Label(card, text="New Category Name:", bg=COLORS["surface"],
                 fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(anchor="w", padx=16)
        self.name_var = tk.StringVar()
        styled_entry(card, self.name_var, width=30).pack(padx=16, fill="x")

        tk.Label(card, text="Color:", bg=COLORS["surface"],
                 fg=COLORS["text_muted"], font=("Segoe UI", 9)).pack(anchor="w", padx=16, pady=(8, 2))
        self.color_var = tk.StringVar(value=self.COLORS_OPTIONS[0])
        color_frame = tk.Frame(card, bg=COLORS["surface"])
        color_frame.pack(padx=16, anchor="w")
        for c in self.COLORS_OPTIONS:
            rb = tk.Radiobutton(color_frame, bg=c, width=2, height=1,
                                 value=c, variable=self.color_var,
                                 relief="flat", bd=2, cursor="hand2",
                                 selectcolor=c)
            rb.pack(side="left", padx=2)

        styled_button(card, "➕ Add Category", self._add,
                      bg=COLORS["accent"], width=26).pack(padx=16, pady=16, fill="x")

    def _load(self):
        self.listbox.delete(0, "end")
        self._cats = TaskController.get_categories(self.user.id)
        for c in self._cats:
            self.listbox.insert("end", f"  {c.name}")

    def _add(self):
        try:
            TaskController.add_category(
                self.name_var.get(), self.color_var.get(), self.user.id)
            self.name_var.set("")
            self._load()
            if self.on_save:
                self.on_save()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)


# ═══════════════════════════════════════════════
#  MAIN APP WINDOW
# ═══════════════════════════════════════════════
class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("TaskFlow — Task Management System")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(bg=COLORS["bg"])
        self._dashboard = None

        # Apply dark theme to Comboboxes
        style = ttk.Style(self)
        style.configure("TCombobox",
                         fieldbackground=COLORS["card"],
                         background=COLORS["card"],
                         foreground=COLORS["text"])

        self.show_login()

    def show_login(self):
        LoginWindow(self, self._on_login)

    def _on_login(self, user):
        if self._dashboard:
            self._dashboard.pack_forget()
            self._dashboard.destroy()
        self._dashboard = DashboardWindow(self, user)
        self.title(f"TaskFlow — {user.username}")


# ═══════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
