# Project Proposal: Assignment & Deadline Manager
<br>

## Problem Statement  

Many students face difficulties in organizing their academic tasks across multiple subjects. With overlapping deadlines and increasing workloads, it becomes easy to forget assignments or submit them late. This often results in:  

- **Late submissions** caused by disorganized tracking.  
- **Missed opportunities** to gain higher grades because tasks are forgotten.  
- **Increased stress and procrastination**, as students struggle to remember due dates.  

Traditional planners or manual notes are often misplaced, forgotten, or too time-consuming to update.  
Therefore, there is a need for a **simple digital solution** that helps students organize their tasks effectively, reminds them of due dates, and improves their time management skills.  
<br>


## Project Objectives  

The main objective of the **Assignment & Deadline Manager** is to provide students with a **lightweight, easy-to-use web app** that helps them manage academic tasks more effectively. Specifically, the project aims to:  

1. **Help students track their assignments and deadlines** in one organized platform.  
2. **Automatically sort tasks by urgency**, ensuring that the most immediate deadlines are visible first.  
3. **Provide deadline reminders** (planned feature) so students can prepare work in advance.  
4. **Promote better time management skills**, reducing last-minute cramming and stress.  
5. **Offer a simple and user-friendly interface** that students of all levels can use without difficulty.  
6. (Planned Extension) **Allow teachers to add class tasks** for their students, so students don’t need to manually input everything.  

By achieving these objectives, this tool will serve as a practical academic planner for both personal use and classroom use.  
<br>



## Planned Features  

The **Assignment & Deadline Manager** will include the following features:  

1. **Add and Manage Assignments**  
   - Students can enter details such as:  
     - Subject name  
     - Task description  
     - Due date  

2. **Automatic Deadline Sorting**  
   - Assignments will be displayed in order of urgency, with the nearest due dates appearing first.  

3. **Deadline Reminders (Planned Feature)**  
   - Notifications will remind students about upcoming deadlines.  
   - This helps prevent late work and forgotten tasks.  

4. **Local Storage for Data**  
   - Assignments will be saved locally on the device.  
   - Data will remain intact even after refreshing or closing the app.  

5. **User-Friendly Design**  
   - Minimal and organized layout.  
   - Easy to navigate for both tech-savvy and non-technical users.  

6. **(Future Feature: Teacher Mode)**  
   - Teachers may input class assignments.  
   - Students can then view these tasks automatically, reducing manual input.  
<br>



## Planned Inputs and Outputs  

### Example Inputs:  
- **Subject Name**: Computer Science  
- **Task Description**: CS-2 Project  
- **Due Date**: September 30, 2025  
<br>


### Example Outputs:  
- **Organized Assignment List**:  
  - "CS-2 Project – Due: September 30, 2025"  
- **Sorted by urgency** so this project will appear at the top if it is the soonest due.  
- (Planned) **Reminders** such as:  
  - "Reminder: CS-2 Project is due in 3 days."  
<br>



## Logic Plan (Pseudocode)  

```pseudocode
START PROGRAM

CREATE an empty list called Assignments

FUNCTION Add_Assignment
    PROMPT user for Subject Name
    PROMPT user for Task Description
    PROMPT user for Due Date (format: YYYY-MM-DD)
    CONVERT Due Date into a date object
    STORE {Subject, Task, Due Date} in Assignments list
    CALL Sort_Assignments
END FUNCTION

FUNCTION Sort_Assignments
    SORT Assignments list by Due Date in ascending order
END FUNCTION

FUNCTION Show_Assignments
    GET today’s date
    FOR each Assignment in Assignments list
        CALCULATE Days_Left = Due Date - Today
        DISPLAY Subject, Task, Due Date, and Days_Left
    END FOR
END FUNCTION

FUNCTION Reminder_Check
    GET today’s date
    FOR each Assignment in Assignments list
        CALCULATE Days_Left = Due Date - Today
        IF Days_Left <= 2 THEN
            DISPLAY "⚠ Reminder: Assignment due soon → " + Subject + " - " + Task
        END IF
    END FOR
END FUNCTION

FUNCTION Save_Data
    WRITE Assignments list to a local file (simulating local storage)
END FUNCTION

FUNCTION Load_Data
    IF saved file exists THEN
        READ Assignments list from the file
    ELSE
        KEEP Assignments list empty
END FUNCTION

REPEAT
    DISPLAY Menu Options:
        1 – Add New Assignment
        2 – Show All Assignments
        3 – Check Reminders
        4 – Exit Program
    PROMPT user for choice

    IF choice = 1 THEN
        CALL Add_Assignment
        CALL Save_Data
    ELSE IF choice = 2 THEN
        CALL Show_Assignments
    ELSE IF choice = 3 THEN
        CALL Reminder_Check
    ELSE IF choice = 4 THEN
        CALL Save_Data
        EXIT PROGRAM
    ELSE
        DISPLAY "Invalid choice. Try again."
UNTIL user chooses Exit

END PROGRAM
