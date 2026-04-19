from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import uuid
from datetime import datetime, date

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "tasktrack_data.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# ---------------- THEMES ----------------

DEFAULT_THEME = {
    "bg": "#1e1f24",
    "card": "#2a2c34",
    "text": "#e6e6e6",
    "accent": "#1e90ff"
}

THEMES = {
    "default": DEFAULT_THEME,
    "blue": {"bg": "#0f172a", "card": "#1e293b", "text": "#e2e8f0", "accent": "#38bdf8"},
    "green": {"bg": "#052e16", "card": "#14532d", "text": "#dcfce7", "accent": "#22c55e"},
    "light": {"bg": "#f5f5f5", "card": "#ffffff", "text": "#111", "accent": "#2563eb"},
}

def load_theme():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_THEME
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return THEMES.get(data.get("theme", "default"), DEFAULT_THEME)
    except:
        return DEFAULT_THEME

def save_theme(theme_name):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"theme": theme_name}, f, indent=4)

# ---------------- DATA ----------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calc_days_left(d):
    try:
        due = datetime.strptime(d, "%Y-%m-%d").date()
        return (due - date.today()).days
    except:
        return 0

def ensure_order(tasks):
    """
    Gives every task an 'order' if missing (important for old JSON files)
    """
    changed = False
    for i, t in enumerate(tasks):
        if "order" not in t:
            t["order"] = i
            changed = True
    return changed

# ---------------- MAIN ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_data()
    error = None
    tab = request.args.get("tab", "home")

    # ADD TASK
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        task = request.form.get("task", "").strip()
        due = request.form.get("due", "").strip()
        priority = request.form.get("priority", "").strip()

        if not subject or not task or not due:
            error = "Please fill out all fields."
        else:
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                error = "Invalid date format."

        if not error:
            tasks.append({
                "id": str(uuid.uuid4()),
                "subject": subject,
                "task": task,
                "due": due,
                "priority": priority,
                "status": "Pending",
                "order": len(tasks)  # 🔥 new task goes last
            })
            save_data(tasks)
            return redirect(url_for("index", tab="tasks"))

    priority_rank = {"High": 3, "Medium": 2, "Low": 1}

    # DAYS LEFT
    for t in tasks:
        t["days_left"] = calc_days_left(t["due"])

    # FIX OLD DATA (important)
    ensure_order(tasks)

    # 🔥 SORT LOGIC (HYBRID SYSTEM)
    tasks.sort(
        key=lambda t: (
            t["status"] == "Completed",   # completed last
            t.get("order", 999999),       # drag & drop order
            datetime.strptime(t["due"], "%Y-%m-%d"),
            -priority_rank.get(t["priority"], 1)
        )
    )

    upcoming = [
        t for t in tasks
        if t["days_left"] >= 0 and t["status"] == "Pending"
    ]

    overdue = [
        t for t in tasks
        if t["days_left"] < 0 and t["status"] == "Pending"
    ]

    completed = [
        t for t in tasks
        if t["status"] == "Completed"
    ]

    theme = load_theme()

    return render_template(
        "index.html",
        tasks=tasks,
        upcoming=upcoming,
        overdue=overdue,
        completed=completed,
        error=error,
        tab=tab,
        theme=theme
    )

# ---------------- DRAG & DROP SAVE ORDER ----------------

@app.route("/reorder", methods=["POST"])
def reorder():
    tasks = load_data()
    new_order = request.json.get("order", [])

    id_map = {t["id"]: t for t in tasks}

    for index, task_id in enumerate(new_order):
        if task_id in id_map:
            id_map[task_id]["order"] = index

    save_data(list(id_map.values()))
    return jsonify({"status": "ok"})

# ---------------- THEME ----------------

@app.route("/set-theme", methods=["POST"])
def set_theme():
    theme = request.form.get("theme", "default")
    save_theme(theme)
    return redirect(url_for("index", tab="settings"))

# ---------------- DONE ----------------

@app.route("/done/<task_id>")
def done(task_id):
    tasks = load_data()

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Completed"
            break

    save_data(tasks)
    return redirect(url_for("index", tab="tasks"))

# ---------------- DELETE ----------------

@app.route("/delete/<task_id>")
def delete(task_id):
    tasks = load_data()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_data(tasks)
    return redirect(url_for("index", tab="tasks"))

# ---------------- EDIT ----------------

@app.route("/edit/<task_id>", methods=["POST"])
def edit(task_id):
    tasks = load_data()

    for t in tasks:
        if t["id"] == task_id:
            t["subject"] = request.form.get("subject")
            t["task"] = request.form.get("task")
            t["due"] = request.form.get("due")
            t["priority"] = request.form.get("priority")
            break

    save_data(tasks)
    return redirect(url_for("index", tab="tasks"))

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)