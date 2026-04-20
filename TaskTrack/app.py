from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os
import re
import uuid
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "Templates"))
app.secret_key = os.environ.get("TASKTRACK_SECRET_KEY", "tasktrack-dev-secret")

DATA_FILE = os.path.join(BASE_DIR, "tasktrack_data.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
TIME_INPUT_RE = re.compile(r"^(0?[1-9]|1[0-2])(?::([0-5][0-9]))?\s*([AaPp][Mm])$")
DEFAULT_DUE_TIME = "23:59"
STATUS_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_SETTINGS = {
    "theme": "default",
    "urgency_highlight_hours": 6,
    "delete_undo_duration": 3,
    "confirm_delete_all_finished": True,
}

# ---------------- THEMES ----------------

DEFAULT_THEME = {
    "bg": "#1e1f24",
    "card": "#2a2c34",
    "text": "#e6e6e6",
    "accent": "#1e90ff",
    "shadow": "rgba(0, 0, 0, 0.28)"
}

THEMES = {
    "default": DEFAULT_THEME,
    "blue": {"bg": "#0f172a", "card": "#1e293b", "text": "#e2e8f0", "accent": "#38bdf8", "shadow": "rgba(15, 23, 42, 0.38)"},
    "light": {"bg": "#eef1f5", "card": "#ffffff", "text": "#1f2937", "accent": "#4f7ecf", "shadow": "rgba(79, 126, 207, 0.10)"},
    "pink": {"bg": "#fdf1f5", "card": "#ffffff", "text": "#4b2a39", "accent": "#d97ca6", "shadow": "rgba(217, 124, 166, 0.12)"},
    "peach": {"bg": "#fdf2ea", "card": "#fffdfb", "text": "#4a3427", "accent": "#dd9367", "shadow": "rgba(221, 147, 103, 0.12)"},
    "sky": {"bg": "#eef6fb", "card": "#fcfeff", "text": "#20384f", "accent": "#6caed6", "shadow": "rgba(108, 174, 214, 0.12)"},
}

def load_settings():
    settings = DEFAULT_SETTINGS.copy()
    if not os.path.exists(SETTINGS_FILE):
        return settings
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return settings
            settings.update(data)
            if settings.get("theme") == "green":
                settings["theme"] = "pink"
            if settings.get("delete_undo_duration") not in {3, 5, 10}:
                settings["delete_undo_duration"] = DEFAULT_SETTINGS["delete_undo_duration"]
            try:
                settings["urgency_highlight_hours"] = int(settings.get("urgency_highlight_hours", DEFAULT_SETTINGS["urgency_highlight_hours"]))
            except (TypeError, ValueError):
                settings["urgency_highlight_hours"] = DEFAULT_SETTINGS["urgency_highlight_hours"]
            settings["urgency_highlight_hours"] = max(1, min(settings["urgency_highlight_hours"], 168))
            settings["confirm_delete_all_finished"] = bool(settings.get("confirm_delete_all_finished", True))
            return settings
    except:
        return settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def update_settings(updates):
    settings = load_settings()
    settings.update(updates)
    save_settings(settings)
    return settings

def load_theme():
    settings = load_settings()
    return THEMES.get(settings.get("theme", "default"), DEFAULT_THEME)

def save_theme(theme_name):
    if theme_name == "green":
        theme_name = "pink"
    update_settings({"theme": theme_name})

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
    transient_keys = {
        "days_left",
        "due_datetime",
        "time_display",
        "due_display",
        "due_status",
        "is_overdue",
        "is_urgent",
        "completed_display",
        "archived_display",
    }
    cleaned = []
    for item in data:
        if isinstance(item, dict):
            cleaned.append({key: value for key, value in item.items() if key not in transient_keys})
        else:
            cleaned.append(item)
    with open(DATA_FILE, "w") as f:
        json.dump(cleaned, f, indent=4)

def calc_days_left(d):
    try:
        due = datetime.strptime(d, "%Y-%m-%d").date()
        return (due - date.today()).days
    except:
        return 0

def parse_time_input(value):
    match = TIME_INPUT_RE.match(value.strip())
    if not match:
        raise ValueError("Invalid time format.")

    hour = int(match.group(1))
    minute = int(match.group(2) or "00")
    meridiem = match.group(3).upper()
    return datetime.strptime(f"{hour}:{minute:02d} {meridiem}", "%I:%M %p")

def normalize_time_input(value):
    return parse_time_input(value).strftime("%H:%M")

def format_time_display(value):
    dt = datetime.strptime(value, "%H:%M")
    return dt.strftime("%I:%M %p").lstrip("0")

def parse_due_datetime(due, due_time):
    return datetime.strptime(f"{due} {due_time}", "%Y-%m-%d %H:%M")

def format_due_display(due, due_time):
    due_dt = parse_due_datetime(due, due_time)
    return due_dt.strftime("%b %d, %Y at %I:%M %p").replace(" 0", " ")

def format_status_timestamp(value):
    if not value:
        return ""
    try:
        dt = datetime.strptime(value, STATUS_TIMESTAMP_FORMAT)
    except ValueError:
        return value
    return dt.strftime("%b %d, %Y at %I:%M %p").replace(" 0", " ")

def normalize_progress_input(value):
    try:
        progress = int(str(value).strip() or "0")
    except (TypeError, ValueError):
        progress = 0
    return max(0, min(progress, 100))

def normalize_checklist_input(value):
    items = value if isinstance(value, list) else []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        normalized.append({
            "text": text,
            "done": bool(item.get("done", False)),
        })
    return normalized[:12]

def humanize_time_diff(total_seconds):
    seconds = abs(int(total_seconds))
    if seconds < 60:
        return "less than a minute"

    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    parts = []
    if days:
        parts.append(f"{days} day(s)")
    if hours:
        parts.append(f"{hours} hour(s)")
    if minutes:
        parts.append(f"{minutes} minute(s)")

    return ", ".join(parts[:3]) if parts else "less than a minute"

def describe_due_status(due_dt):
    delta_seconds = int((due_dt - datetime.now()).total_seconds())
    if abs(delta_seconds) < 60:
        return "Due now"
    if delta_seconds > 0:
        return f"Due in {humanize_time_diff(delta_seconds)}"
    return f"Overdue by {humanize_time_diff(delta_seconds)}"

def ensure_time(tasks):
    changed = False
    for t in tasks:
        if "time" not in t or not t["time"]:
            t["time"] = DEFAULT_DUE_TIME
            changed = True
        if "notes" not in t:
            t["notes"] = ""
            changed = True
        if "completed_at" not in t:
            t["completed_at"] = ""
            changed = True
        if "archived_at" not in t:
            t["archived_at"] = ""
            changed = True
        if "progress" not in t:
            t["progress"] = 0
            changed = True
        else:
            normalized_progress = normalize_progress_input(t.get("progress"))
            if normalized_progress != t.get("progress"):
                t["progress"] = normalized_progress
                changed = True
        if "checklist" not in t:
            t["checklist"] = []
            changed = True
        else:
            normalized_checklist = normalize_checklist_input(t.get("checklist"))
            if normalized_checklist != t.get("checklist"):
                t["checklist"] = normalized_checklist
                changed = True
    return changed

def has_custom_order(tasks):
    return any("manual_order" in t for t in tasks)

def filter_tasks(tasks, search_query=""):
    filtered = tasks
    if search_query:
        query = search_query.lower()
        filtered = [
            t for t in filtered
            if query in t.get("subject", "").lower()
            or query in t.get("task", "").lower()
            or query in t.get("priority", "").lower()
            or query in t.get("notes", "").lower()
        ]
    return filtered

def get_recent_actions():
    actions = session.get("recent_actions", [])
    now_ts = datetime.now().timestamp()
    actions = [item for item in actions if now_ts <= item.get("expires_at", 0)]
    session["recent_actions"] = actions
    return actions

def push_recent_action(action):
    actions = get_recent_actions()
    actions.append(action)
    session["recent_actions"] = actions[-6:]

# ---------------- MAIN ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    settings = load_settings()
    tasks = load_data()
    error = None
    tab = request.args.get("tab", "home")
    task_panel = request.args.get("task_panel", "active")
    search_query = request.args.get("q", "").strip()
    if task_panel not in {"active", "finished", "archived"}:
        task_panel = "active"

    # ADD TASK
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        task = request.form.get("task", "").strip()
        due = request.form.get("due", "").strip()
        due_time_input = request.form.get("time", "").strip()
        priority = request.form.get("priority", "").strip()
        notes = request.form.get("notes", "").strip()
        progress = normalize_progress_input(request.form.get("progress", "0"))

        if not subject or not task or not due or not due_time_input:
            error = "Please fill out all fields."
        else:
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                error = "Invalid date format."
            try:
                due_time = normalize_time_input(due_time_input)
            except ValueError:
                error = "Invalid time format. Use times like 3:30 PM."

        if not error:
            next_manual_order = None
            if has_custom_order(tasks):
                next_manual_order = max((t.get("manual_order", -1) for t in tasks), default=-1) + 1

            new_task = {
                "id": str(uuid.uuid4()),
                "subject": subject,
                "task": task,
                "due": due,
                "time": due_time,
                "priority": priority,
                "notes": notes,
                "progress": progress,
                "status": "Pending",
            }

            if next_manual_order is not None:
                new_task["manual_order"] = next_manual_order

            tasks.append({
                **new_task
            })
            save_data(tasks)
            push_recent_action({
                "id": str(uuid.uuid4()),
                "type": "remove_added_task",
                "task_id": new_task["id"],
                "expires_at": datetime.now().timestamp() + settings.get("delete_undo_duration", 3),
                "label": f"{subject} added.",
                "tab": "tasks",
                "task_panel": "active",
            })
            return redirect(url_for("index", tab="tasks", task_panel="active"))

    priority_rank = {"High": 3, "Medium": 2, "Low": 1}

    changed = False
    if ensure_time(tasks):
        changed = True

    now = datetime.now()
    urgency_window_seconds = settings.get("urgency_highlight_hours", DEFAULT_SETTINGS["urgency_highlight_hours"]) * 3600
    for t in tasks:
        t["days_left"] = calc_days_left(t["due"])
        due_dt = parse_due_datetime(t["due"], t["time"])
        delta_seconds = int((due_dt - now).total_seconds())
        t["due_datetime"] = due_dt
        t["time_display"] = format_time_display(t["time"])
        t["due_display"] = format_due_display(t["due"], t["time"])
        t["due_status"] = describe_due_status(due_dt)
        t["is_overdue"] = t["status"] == "Pending" and due_dt < now
        t["is_urgent"] = t["status"] == "Pending" and 0 <= delta_seconds <= urgency_window_seconds
        t["completed_display"] = format_status_timestamp(t.get("completed_at", ""))
        t["archived_display"] = format_status_timestamp(t.get("archived_at", ""))
        t["checklist_total"] = len(t.get("checklist", []))
        t["checklist_done"] = sum(1 for item in t.get("checklist", []) if item.get("done"))

    if changed:
        save_data(tasks)

    use_custom_order = has_custom_order(tasks)
    if use_custom_order:
        tasks.sort(
            key=lambda t: (
                t["status"] != "Pending",
                t["status"] == "Archived",
                t.get("manual_order", 999999),
                t["due_datetime"],
                -priority_rank.get(t["priority"], 1)
            )
        )
    else:
        tasks.sort(
            key=lambda t: (
                t["status"] != "Pending",
                t["status"] == "Archived",
                t["due_datetime"],
                -priority_rank.get(t["priority"], 1),
                t["subject"].lower(),
                t["task"].lower()
            )
        )

    upcoming = [
        t for t in tasks
        if not t["is_overdue"] and t["status"] == "Pending"
    ]

    pending_tasks = [
        t for t in tasks
        if t["status"] == "Pending"
    ]

    overdue = [
        t for t in tasks
        if t["is_overdue"] and t["status"] == "Pending"
    ]

    completed = [
        t for t in tasks
        if t["status"] == "Completed"
    ]

    archived = [
        t for t in tasks
        if t["status"] == "Archived"
    ]

    filtered_pending_tasks = filter_tasks(pending_tasks, search_query)
    filtered_completed_tasks = filter_tasks(completed, search_query)
    filtered_archived_tasks = filter_tasks(archived, search_query)
    can_reorder = not search_query
    recent_actions = get_recent_actions()

    theme = THEMES.get(settings.get("theme", "default"), DEFAULT_THEME)

    return render_template(
        "index.html",
        tasks=tasks,
        pending_tasks=pending_tasks,
        filtered_pending_tasks=filtered_pending_tasks,
        upcoming=upcoming,
        overdue=overdue,
        completed=completed,
        filtered_completed_tasks=filtered_completed_tasks,
        archived=archived,
        filtered_archived_tasks=filtered_archived_tasks,
        recent_actions=recent_actions,
        search_query=search_query,
        can_reorder=can_reorder,
        settings=settings,
        has_custom_order=has_custom_order(tasks),
        error=error,
        tab=tab,
        task_panel=task_panel,
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
            id_map[task_id]["manual_order"] = index

    save_data(list(id_map.values()))
    return jsonify({"status": "ok"})

@app.route("/reset-order")
def reset_order():
    tasks = load_data()
    previous_orders = {
        task["id"]: task.get("manual_order")
        for task in tasks
        if "manual_order" in task
    }
    for task in tasks:
        task.pop("manual_order", None)
    save_data(tasks)
    if previous_orders:
        push_recent_action({
            "id": str(uuid.uuid4()),
            "type": "restore_order",
            "orders": previous_orders,
            "expires_at": datetime.now().timestamp() + load_settings().get("delete_undo_duration", 3),
            "label": "Custom order cleared.",
            "tab": "tasks",
            "task_panel": "active",
        })
    return redirect(url_for("index", tab="tasks", task_panel="active"))

# ---------------- THEME ----------------

@app.route("/save-settings", methods=["POST"])
def save_settings_route():
    theme = request.form.get("theme", DEFAULT_SETTINGS["theme"])
    if theme == "green":
        theme = "pink"

    settings = load_settings()
    settings.update({
        "theme": theme if theme in THEMES else DEFAULT_SETTINGS["theme"],
        "confirm_delete_all_finished": request.form.get("confirm_delete_all_finished") == "on",
    })

    try:
        urgency_highlight_hours = int(request.form.get("urgency_highlight_hours", DEFAULT_SETTINGS["urgency_highlight_hours"]))
    except ValueError:
        urgency_highlight_hours = DEFAULT_SETTINGS["urgency_highlight_hours"]
    settings["urgency_highlight_hours"] = max(1, min(urgency_highlight_hours, 168))

    try:
        delete_undo_duration = int(request.form.get("delete_undo_duration", DEFAULT_SETTINGS["delete_undo_duration"]))
    except ValueError:
        delete_undo_duration = DEFAULT_SETTINGS["delete_undo_duration"]

    if delete_undo_duration not in {3, 5, 10}:
        delete_undo_duration = DEFAULT_SETTINGS["delete_undo_duration"]
    settings["delete_undo_duration"] = delete_undo_duration

    save_settings(settings)
    return redirect(url_for("index", tab="settings"))

@app.route("/set-theme", methods=["POST"])
def set_theme():
    theme = request.form.get("theme", DEFAULT_SETTINGS["theme"])
    save_theme(theme)
    return redirect(url_for("index", tab="settings"))

# ---------------- DONE ----------------

@app.route("/done/<task_id>")
def done(task_id):
    tasks = load_data()

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Completed"
            t["completed_at"] = datetime.now().strftime(STATUS_TIMESTAMP_FORMAT)
            t["archived_at"] = ""
            break

    save_data(tasks)
    return redirect(url_for("index", tab="tasks", task_panel="finished"))

@app.route("/undo/<task_id>")
def undo(task_id):
    tasks = load_data()

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Pending"
            t["completed_at"] = ""
            t["archived_at"] = ""
            break

    save_data(tasks)
    return redirect(url_for("index", tab="tasks", task_panel="finished"))

@app.route("/restore-finished")
def restore_finished():
    tasks = load_data()
    changed = False
    for task in tasks:
        if task.get("status") == "Completed":
            task["status"] = "Pending"
            task["completed_at"] = ""
            task["archived_at"] = ""
            changed = True
    if changed:
        save_data(tasks)
    return redirect(url_for("index", tab="tasks", task_panel="finished"))

@app.route("/archive/<task_id>")
def archive(task_id):
    tasks = load_data()

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Archived"
            if not t.get("completed_at"):
                t["completed_at"] = datetime.now().strftime(STATUS_TIMESTAMP_FORMAT)
            t["archived_at"] = datetime.now().strftime(STATUS_TIMESTAMP_FORMAT)
            break

    save_data(tasks)
    return redirect(url_for("index", tab="tasks", task_panel="archived"))

@app.route("/restore-archived/<task_id>")
def restore_archived(task_id):
    tasks = load_data()

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Pending"
            t["completed_at"] = ""
            t["archived_at"] = ""
            break

    save_data(tasks)
    return redirect(url_for("index", tab="tasks", task_panel="archived"))

# ---------------- DELETE ----------------

@app.route("/delete/<task_id>")
def delete(task_id):
    tasks = load_data()
    task_to_delete = next((t for t in tasks if t["id"] == task_id), None)
    tasks = [t for t in tasks if t["id"] != task_id]
    save_data(tasks)
    if task_to_delete:
        settings = load_settings()
        push_recent_action({
            "id": task_to_delete.get("id"),
            "type": "restore_task",
            "task": task_to_delete,
            "expires_at": datetime.now().timestamp() + settings.get("delete_undo_duration", 3),
            "tab": request.args.get("tab", "tasks"),
            "task_panel": request.args.get("task_panel", "active"),
            "label": task_to_delete.get("subject", "Task"),
        })
    return redirect(url_for("index", tab=request.args.get("tab", "tasks"), task_panel=request.args.get("task_panel", "active")))

@app.route("/undo-action/<action_id>")
def undo_action(action_id):
    recent_actions = get_recent_actions()
    action = next((item for item in recent_actions if item.get("id") == action_id), None)
    if not action:
        return redirect(url_for("index", tab="tasks", task_panel="active"))

    tasks = load_data()
    action_type = action.get("type")

    if action_type == "remove_added_task":
        tasks = [task for task in tasks if task.get("id") != action.get("task_id")]
        save_data(tasks)
    elif action_type == "restore_task":
        task = action.get("task")
        if task and not any(existing.get("id") == task.get("id") for existing in tasks):
            tasks.append(task)
            save_data(tasks)
    elif action_type == "restore_tasks":
        changed = False
        for task in action.get("tasks", []):
            if not any(existing.get("id") == task.get("id") for existing in tasks):
                tasks.append(task)
                changed = True
        if changed:
            save_data(tasks)
    elif action_type == "restore_order":
        order_map = action.get("orders", {})
        changed = False
        for task in tasks:
            task_id = task.get("id")
            if task_id in order_map:
                task["manual_order"] = order_map[task_id]
                changed = True
        if changed:
            save_data(tasks)

    tab = action.get("tab", "tasks")
    task_panel = action.get("task_panel", "active")
    session["recent_actions"] = [item for item in recent_actions if item.get("id") != action_id]
    return redirect(url_for("index", tab=tab, task_panel=task_panel))

@app.route("/delete-completed")
def delete_completed():
    tasks = load_data()
    deleted_tasks = [t for t in tasks if t["status"] == "Completed"]
    tasks = [t for t in tasks if t["status"] != "Completed"]
    save_data(tasks)
    if deleted_tasks:
        push_recent_action({
            "id": str(uuid.uuid4()),
            "type": "restore_tasks",
            "tasks": deleted_tasks,
            "expires_at": datetime.now().timestamp() + load_settings().get("delete_undo_duration", 3),
            "label": f"{len(deleted_tasks)} finished task(s) cleared.",
            "tab": "tasks",
            "task_panel": "finished",
        })
    return redirect(url_for("index", tab="tasks", task_panel="finished"))

# ---------------- EDIT ----------------

@app.route("/edit/<task_id>", methods=["POST"])
def edit(task_id):
    tasks = load_data()
    subject = request.form.get("subject", "").strip()
    task = request.form.get("task", "").strip()
    due = request.form.get("due", "").strip()
    due_time_input = request.form.get("time", "").strip()
    priority = request.form.get("priority", "").strip()
    progress = normalize_progress_input(request.form.get("progress", "0"))

    if not subject or not task or not due or not due_time_input:
        return redirect(url_for("index", tab="tasks", task_panel="active"))

    try:
        datetime.strptime(due, "%Y-%m-%d")
        due_time = normalize_time_input(due_time_input)
    except ValueError:
        return redirect(url_for("index", tab="tasks", task_panel="active"))

    for t in tasks:
        if t["id"] == task_id:
            t["subject"] = subject
            t["task"] = task
            t["due"] = due
            t["time"] = due_time
            t["priority"] = priority
            t["progress"] = progress
            break

    save_data(tasks)
    return redirect(url_for("index", tab="tasks", task_panel="active"))

@app.route("/edit-note/<task_id>", methods=["POST"])
def edit_note(task_id):
    tasks = load_data()
    notes = request.form.get("notes", "").strip()
    checklist_raw = request.form.get("checklist", "[]")
    try:
        checklist = normalize_checklist_input(json.loads(checklist_raw))
    except json.JSONDecodeError:
        checklist = []

    for t in tasks:
        if t["id"] == task_id:
            t["notes"] = notes
            t["checklist"] = checklist
            break

    save_data(tasks)

    task_panel = request.form.get("task_panel", "active")
    if task_panel not in {"active", "finished", "archived"}:
        task_panel = "active"
    return redirect(url_for("index", tab="tasks", task_panel=task_panel))

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
