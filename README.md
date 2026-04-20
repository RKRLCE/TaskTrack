# TaskTrack: An Assignment Tracker App

TaskTrack is a student-focused web app that helps organize assignments, deadlines, and priorities in one clean workspace. It is designed for students who need a simple way to stay on top of school tasks, avoid missed submissions, and manage their workload with less stress.

The app lets users add assignments, set due dates and due times, assign priorities, update task details, and monitor which work is upcoming, overdue, or already finished. It also supports optional drag-and-drop reordering when a student wants to override the default automatic task order.

---

## Overview

Managing multiple assignments across different subjects can quickly become overwhelming. Students often deal with:

- Missed deadlines because tasks are scattered or forgotten
- Late submissions caused by poor time tracking
- Higher stress levels from disorganized schedules
- Difficulty deciding which assignment should be done first

TaskTrack was created to solve these problems through a focused and accessible task tracker for students. It combines deadline tracking, priority organization, status management, and a user-friendly interface so students can plan their work more clearly.

---

## Current Features

### 1. Add and Manage Assignments
Users can create tasks with:

- Subject name
- Task description
- Due date
- Due time
- Priority level

### 2. Edit Assignment Details
Assignments can be updated after creation, including:

- Subject
- Task description
- Due date
- Due time
- Priority

### 3. Status Tracking
Each assignment is tracked by status:

- Pending
- Completed

Pending tasks stay in the main active list, while completed tasks are moved into a finished section inside the Tasks page.

### 4. Finished Tasks Section
Completed assignments are separated from active work through a built-in finished tasks subview. From there, users can:

- Review completed work
- Undo a completed task if it was marked by mistake
- Delete an individual finished task
- Delete all finished tasks at once

### 5. Automatic Sorting with Optional Manual Reordering
By default, TaskTrack automatically sorts active tasks by:

1. Due date and time
2. Priority level

If the user prefers a custom arrangement, tasks can also be drag-and-dropped into a manual order. Once dragged, that order becomes the saved custom arrangement.

### 6. Due-Time-Aware Urgency Tracking
TaskTrack does not only track dates. It also checks the actual due time and shows messages such as:

- Due in 2 hours
- Due in 1 day, 3 hours
- Overdue by 45 minutes

This gives students a clearer idea of exactly how urgent a task is.

### 7. Upcoming and Overdue Sections
The Home page highlights:

- Upcoming assignments
- Overdue assignments
- Total assignment count

This helps users quickly understand their workload at a glance.

### 8. Multiple Theme Options
The app includes several visual themes, including:

- Default
- Blue
- Light
- Pink
- Peach
- Sky

These themes allow students to personalize the interface while keeping it readable and organized.

### 9. Local JSON-Based Data Storage
Task data and theme preferences are stored locally using JSON files. This allows the app to preserve tasks and settings without requiring an external database.

### 10. Improved User Interface
The interface is built to feel more spacious and easier to use, with:

- Wider layout for better screen usage
- Clear task cards
- More obvious action buttons
- Separate active and finished task views inside the Tasks section
- A cleaner dashboard for overdue and upcoming work

---

## Inputs

### Example Task Input

- Subject Name: Computer Science
- Task Description: Final project presentation
- Due Date: September 30, 2025
- Due Time: 3:30 PM
- Priority Level: High

---

## Outputs

### Example Task Display

- Computer Science
- Final project presentation
- Due: Sep 30, 2025 at 3:30 PM
- Priority: High
- Status: Due in 2 days, 4 hours

### Example Finished Task Actions

- Undo Finish
- Delete Task
- Delete All Finished

---

## Purpose

TaskTrack was developed to support better student productivity and time management. Instead of relying on scattered notes or memory, students can use one organized platform to monitor deadlines, decide what matters most, and reduce the chances of forgetting important work.

---

## Contributors

- Rayen Leigh C. Elecho
- Jerriel Aljamz L. Salih
