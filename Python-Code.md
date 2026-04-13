## Run using VS Code and open the window loaded
````
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime, date
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
    def sort_key(a):
        due = datetime.strptime(a["due"], "%m-%d-%Y").date()
        overdue = due < date.today() and a["status"] == "Pending"
        return (not overdue, due, {"High": 0, "Medium": 1, "Low": 2}[a["priority"]])
    assignments.sort(key=sort_key)

def days_left(d):
    due = datetime.strptime(d, "%m-%d-%Y").date()
    return (due - date.today()).days

# -------------------- Popup Form --------------------

def assignment_popup(edit_idx=None):
    popup = Toplevel(root)
    popup.title("Assignment")
    popup.grab_set()
    popup.resizable(False, False)

    is_edit = edit_idx is not None
    data = assignments[edit_idx] if is_edit else {
        "subject": "",
        "task": "",
        "due": "",
        "priority": "Medium",
        "status": "Pending"
    }

    ttk.Label(popup, text="Assignment Details", font=("Segoe UI", 14, "bold")).pack(pady=10)

    frame = Frame(popup)
    frame.pack(padx=15, pady=10)

    ttk.Label(frame, text="Subject").grid(row=0, column=0, sticky="w", pady=4)
    subj = Entry(frame, width=30)
    subj.grid(row=0, column=1, pady=4)
    subj.insert(0, data["subject"])

    ttk.Label(frame, text="Task Description").grid(row=1, column=0, sticky="w", pady=4)
    task = Entry(frame, width=45)
    task.grid(row=1, column=1, pady=4)
    task.insert(0, data["task"])

    ttk.Label(frame, text="Due Date (MM-DD-YYYY)").grid(row=2, column=0, sticky="w", pady=4)
    due = Entry(frame, width=20)
    due.grid(row=2, column=1, pady=4)
    due.insert(0, data["due"])

    ttk.Label(frame, text="Priority").grid(row=3, column=0, sticky="w", pady=4)
    priority = ttk.Combobox(
        frame,
        values=["Low", "Medium", "High"],
        state="readonly",
        width=18
    )
    priority.grid(row=3, column=1, sticky="w", pady=4)
    priority.set(data["priority"])

    def save():
        if not subj.get() or not task.get() or not due.get():
            messagebox.showwarning("Missing Info", "Please complete all fields.")
            return

        try:
            datetime.strptime(due.get(), "%m-%d-%Y")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use MM-DD-YYYY format.")
            return

        new_data = {
            "subject": subj.get(),
            "task": task.get(),
            "due": due.get(),
            "priority": priority.get(),
            "status": data["status"]
        }

        if is_edit:
            assignments[edit_idx] = new_data
        else:
            assignments.append(new_data)

        sort_assignments()
        save_data()
        popup.destroy()
        show_tasks()

    btns = Frame(popup)
    btns.pack(pady=10)

    Button(btns, text="Save" if not is_edit else "Update", width=14, command=save).pack(side=LEFT, padx=6)
    Button(btns, text="Cancel", width=14, command=popup.destroy).pack(side=LEFT, padx=6)

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
        text=(
            "TaskTrack helps students organize assignments,\n"
            "monitor due dates, and manage academic tasks\n"
            "in a simple and structured way."
        ),
        font=("Segoe UI", 14),
        fg="gray",
        justify="center"
    ).pack()

def show_tasks():
    clear_content()

    header = Frame(content)
    header.pack(fill=X, pady=10)

    Label(header, text="Assignments", font=("Segoe UI", 20, "bold")).pack(side=LEFT)
    Button(header, text="Add Assignment", command=lambda: assignment_popup()).pack(side=RIGHT)

    search_entry = Entry(content)
    search_entry.pack(fill=X, padx=10, pady=5)
    search_entry.insert(0, "Search assignments")

    list_frame = Frame(content)
    list_frame.pack(fill=BOTH, expand=True)

    def refresh():
        for w in list_frame.winfo_children():
            w.destroy()

        query = search_entry.get().lower()

        for idx, a in enumerate(assignments):
            if query and query != "search assignments":
                if query not in (a["subject"] + a["task"]).lower():
                    continue

            card = Frame(list_frame, bd=1, relief="solid", padx=10, pady=6)
            card.pack(fill=X, padx=10, pady=4)

            bg = {"High": "#ffe0e0", "Medium": "#fff2cc", "Low": "#e6ffe6"}[a["priority"]]
            card.config(bg=bg)

            remaining = days_left(a["due"])
            status_text = a["status"]

            info = f"{a['subject']} | {a['task']} | Due: {a['due']}"
            if remaining < 0:
                info += f" | Overdue by {abs(remaining)} days"
            elif remaining == 0:
                info += " | Due today"

            Label(card, text=info, bg=bg).pack(anchor="w")
            Label(
                card,
                text=f"Priority: {a['priority']} | Status: {status_text}",
                bg=bg,
                fg="gray"
            ).pack(anchor="w")

            actions = Frame(card, bg=bg)
            actions.pack(anchor="e")

            Button(actions, text="Edit", command=lambda i=idx: assignment_popup(i)).pack(side=LEFT, padx=4)

            Button(
                actions,
                text="Finished",
                command=lambda i=idx: mark_finished(i),
                bg="#4caf50",
                fg="white"
            ).pack(side=LEFT, padx=4)

            Button(
                actions,
                text="Delete",
                command=lambda i=idx: delete_task(i),
                bg="#f44336",
                fg="white"
            ).pack(side=LEFT, padx=4)

    def mark_finished(i):
        assignments[i]["status"] = "Completed"
        save_data()
        refresh()

    def delete_task(i):
        if messagebox.askyesno("Delete Assignment", "Are you sure you want to delete this assignment?"):
            assignments.pop(i)
            save_data()
            refresh()

    search_entry.bind("<KeyRelease>", lambda e: refresh())
    refresh()

def show_about():
    clear_content()

    Label(content, text="About TaskTrack", font=("Segoe UI", 22, "bold")).pack(pady=20)

    Label(
        content,
        text=(
            "TaskTrack is an assignment tracker created to help students\n"
            "manage schoolwork by organizing tasks, monitoring deadlines,\n"
            "and tracking assignment completion.\n\n"
            "Creators:\n"
            "Rayen Leigh C. Elecho\n"
            "Jerriel Aljamz L. Salih"
        ),
        font=("Segoe UI", 12),
        justify="center"
    ).pack()

# -------------------- Layout --------------------

root = Tk()
root.title("TaskTrack")
root.geometry("980x620")
root.resizable(False, False)

nav = Frame(root, bg="#1e90ff", height=50)
nav.pack(fill=X)
nav.pack_propagate(False)

def nav_btn(text, cmd):
    Button(
        nav,
        text=text,
        bg="#1e90ff",
        fg="white",
        bd=0,
        font=("Segoe UI", 12),
        command=cmd
    ).pack(side=LEFT, padx=20)

nav_btn("Home", show_home)
nav_btn("Assignments", show_tasks)
nav_btn("About Us", show_about)

content = Frame(root, bg="white")
content.pack(fill=BOTH, expand=True)

# -------------------- Start --------------------

load_data()
sort_assignments()
show_home()

root.mainloop()


````
