# Project Proposal: Assignment & Deadline Manager
<br>

## Problem Statement  
Many students struggle to keep track of multiple assignments and deadlines, which often leads to late submissions.  
Without proper reminders, it is easy to forget tasks or manage time poorly.  
There is a need for a tool that organizes subjects and due dates while reminding students of upcoming deadlines.  
<br>

## Project Objectives  
The main goal of the **Assignment & Deadline Manager** is to give students a **simple web app** to manage school work. Specifically, it aims to:  

1. **Help students keep track of assignments and deadlines** in one place.  
2. **Sort tasks by how urgent they are**, so the soonest deadlines show first.  
3. **Send reminders for deadlines** (planned feature) so students can finish work on time.  
4. **Help students manage their time better**, avoiding last-minute work and stress.  
5. **Have an easy-to-use interface** that everyone can understand.  
<br>

## Planned Features  
The **Assignment & Deadline Manager** will have these features:  

1. **Add and Manage Assignments**  
   - Students can type:  
     - Subject name  
     - Task description  
     - Due date  

2. **Automatic Deadline Sorting**  
   - Tasks show up with the soonest deadlines first.  

3. **Deadline Reminders (Planned Feature)**  
   - Notifications remind students of upcoming tasks.  

4. **Local Storage for Data**  
   - Tasks are saved on the device.  
   - Data stays even after closing or refreshing the app.  

5. **User-Friendly Design**  
   - Clean, simple layout.  
   - Easy to use for everyone.  
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
- **Sorted by urgency** so the nearest deadlines show first.  
- (Planned) **Reminders** like:  
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
