# Compile Using:
## https://codehs.com/sandbox/id/python-graphics-tkinter-IPnUun

````
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import json
import os

# -------------------- App State --------------------

DATA_FILE = "tasktrack_data.json"
assignments = []

# -------------------- File Handling --------------------

def load_data():
    global assignments
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            assignments = json.load(f)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(assignments, f, indent=4)

# -------------------- Utilities --------------------

def clear_content():
    for w in content.winfo_children():
        w.destroy()

def sort_assignments():
    assignments.sort(key=lambda x: x["due_date"])

def days_left(due):
    today = datetime.now().date()
    due_date = datetime.strptime(due, "%Y-%m-%d").date()
    return (due_date - today).days

# -------------------- Pages --------------------

def show_home():
    clear_content()

    Label(
        content,
        text="Welcome to TaskTrack",
        font=("Segoe UI", 26, "bold")
    ).pack(pady=40)

    Label(
        content,
        text="Track assignments. Manage deadlines. Stay organized.",
        font=("Segoe UI", 14),
        fg="gray"
    ).pack()

def show_create():
    clear_content()

    Label(
        content,
        text="Create Assignment",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=20)

    form = Frame(content)
    form.pack(pady=10)

    Label(form, text="Subject").grid(row=0, column=0, sticky="w", pady=6)
    Label(form, text="Task Description").grid(row=1, column=0, sticky="w", pady=6)
    Label(form, text="Due Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", pady=6)

    subject_entry = Entry(form, width=30)
    task_entry = Entry(form, width=45)
    due_entry = Entry(form, width=20)

    subject_entry.grid(row=0, column=1, pady=6)
    task_entry.grid(row=1, column=1, pady=6)
    due_entry.grid(row=2, column=1, pady=6)

    def add_task():
        subject = subject_entry.get().strip()
        task = task_entry.get().strip()
        due = due_entry.get().strip()

        if not subject or not task or not due:
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use YYYY-MM-DD format.")
            return

        assignments.append({
            "subject": subject,
            "task": task,
            "due_date": due
        })

        sort_assignments()
        save_data()

        subject_entry.delete(0, END)
        task_entry.delete(0, END)
        due_entry.delete(0, END)

        messagebox.showinfo("Success", "Assignment added successfully.")

    Button(
        content,
        text="Add Assignment",
        command=add_task,
        bg="#1e90ff",
        fg="white",
        width=26
    ).pack(pady=20)

def show_tasks():
    clear_content()

    Label(
        content,
        text="Your Assignments",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=20)

    listbox = Listbox(content, width=95, height=15)
    listbox.pack(pady=10)

    for a in assignments:
        remaining = days_left(a["due_date"])
        text = f"{a['subject']} | {a['task']} | Due: {a['due_date']} | Days Left: {remaining}"
        listbox.insert(END, text)

        if remaining <= 2:
            listbox.itemconfig(END, bg="#ffd6d6")

def show_about():
    clear_content()

    Label(
        content,
        text="About TaskTrack",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=20)

    Label(
        content,
        text=(
            "TaskTrack is a simple assignment tracker designed to help students\n"
            "organize tasks, track deadlines, and avoid late submissions.\n\n"
            "It promotes better time management through an easy-to-use interface."
        ),
        font=("Segoe UI", 12),
        justify="center"
    ).pack(pady=10)

    Label(
        content,
        text="Creators",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(20, 5))

    Label(
        content,
        text=(
            "Rayen Leigh C. Elecho\n"
            "Jerriel Aljamz L. Salih"
        ),
        font=("Segoe UI", 12),
        justify="center"
    ).pack()

# -------------------- UI Layout --------------------

root = Tk()
root.title("TaskTrack")
root.geometry("900x600")
root.resizable(False, False)

# Top Navigation Bar
top_bar = Frame(root, bg="#1e90ff", height=55)
top_bar.pack(fill=X)
top_bar.pack_propagate(False)

def nav(text, cmd):
    Button(
        top_bar,
        text=text,
        font=("Segoe UI", 12),
        bg="#1e90ff",
        fg="white",
        bd=0,
        command=cmd
    ).pack(side=LEFT, padx=20)

nav("Home", show_home)
nav("Create Task", show_create)
nav("View Tasks", show_tasks)
nav("About Us", show_about)

# Content Area
content = Frame(root, bg="white")
content.pack(fill=BOTH, expand=True)

# -------------------- Start App --------------------

load_data()
sort_assignments()
show_home()

root.mainloop()

````
