import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY,
                  description TEXT,
                  priority TEXT,
                  due_date TEXT,
                  completed INTEGER)''')
    conn.commit()
    conn.close()

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("800x400")
        self.root.configure(bg="#f0f0f0")  # Light grey background for the main window

        # Frame for task input
        self.input_frame = tk.Frame(root, padx=10, pady=10, bg="#e6f7ff")  # Light blue background for input frame
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Task Description", bg="#e6f7ff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.description_entry = tk.Entry(self.input_frame, width=30)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Priority (high, medium, low)", bg="#e6f7ff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.priority_entry = tk.Entry(self.input_frame, width=30)
        self.priority_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Due Date (YYYY-MM-DD)", bg="#e6f7ff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.due_date_entry = tk.Entry(self.input_frame, width=30)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.input_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame for task list
        self.list_frame = tk.Frame(root, padx=10, pady=10, bg="#d9f7be")  # Light green background for list frame
        self.list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.list_button = tk.Button(self.list_frame, text="List Tasks", command=self.list_tasks)
        self.list_button.pack(side=tk.TOP, pady=5)

        columns = ("ID", "Description", "Priority", "Due Date", "Status")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)

        self.buttons_frame = tk.Frame(root, padx=10, pady=10, bg="#fff4e6")  # Light orange background for buttons frame
        self.buttons_frame.pack(pady=10)

        self.remove_button = tk.Button(self.buttons_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.grid(row=0, column=0, padx=5, pady=5)

        self.mark_button = tk.Button(self.buttons_frame, text="Mark as Completed", command=self.mark_task_completed)
        self.mark_button.grid(row=0, column=1, padx=5, pady=5)

        self.init_db()

    def init_db(self):
        init_db()

    def add_task(self):
        description = self.description_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()

        if not description or not priority or not due_date:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Due date must be in YYYY-MM-DD format")
            return

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (description, priority, due_date, completed) VALUES (?, ?, ?, 0)",
                  (description, priority, due_date))
        conn.commit()
        conn.close()

        self.description_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

        self.list_tasks()

    def list_tasks(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("SELECT id, description, priority, due_date, completed FROM tasks")
        tasks = c.fetchall()
        conn.close()

        for task in tasks:
            self.tree.insert("", "end", values=(task[0], task[1], task[2], task[3], 'Completed' if task[4] else 'Pending'))

    def remove_task(self):
        selected_item = self.tree.selection()[0]
        task_id = self.tree.item(selected_item)['values'][0]

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

        self.tree.delete(selected_item)

    def mark_task_completed(self):
        selected_item = self.tree.selection()[0]
        task_id = self.tree.item(selected_item)['values'][0]

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

        self.list_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
