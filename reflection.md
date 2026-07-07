# PawPal+ Project Reflection

## 1. System Design

### a. Initial design

My initial UML design focused on separating responsibilities across five classes: Owner, Pet, Task, Scheduler, and Plan. The Owner class stores information about the pet owner and manages multiple pets. Each Pet stores its own information and a list of assigned tasks. The Task class represents individual pet care activities, including the due date, due time, priority, duration, recurrence, and completion status. The Scheduler class contains the application's core scheduling logic, such as sorting, filtering, conflict detection, and recurring task generation. Finally, the Plan class formats the generated schedule into a readable output for both the CLI and Streamlit application.

### b. Design changes

During implementation, I simplified the Pet class by removing the age attribute because it was not being used in the scheduling logic. I also added the Plan class after beginning development because separating the scheduling logic from the display logic made the code easier to organize and maintain. Another change was adding recurring task generation after a task is completed, which was not part of my original design.

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

The scheduler considers task priority, due time, completion status, and recurring frequency. High-priority tasks are scheduled before medium- and low-priority tasks, and tasks with the same priority are ordered by their scheduled time. The scheduler also detects conflicts when two incomplete tasks occur at the same date and time. I chose these constraints because they are the most important factors in helping a pet owner complete essential care tasks efficiently.

### b. Tradeoffs

One tradeoff in my scheduler is that priority is considered before task duration. This means that a longer high-priority task may appear before a shorter low-priority task. I chose this approach because ensuring that critical pet care tasks, such as medication or feeding, are completed on time is more important than minimizing the total schedule length.

---

## 3. AI Collaboration

### a. How you used AI

I used AI throughout the project to help design the class structure, improve my UML diagram, debug Python code, write unit tests, and connect my backend classes to the Streamlit interface. The most helpful prompts were those asking for step-by-step explanations of object-oriented programming concepts and suggestions for improving the scheduler while keeping the code organized.

### b. Judgment and verification

I did not accept every AI suggestion without verifying it. For example, after modifying the Pet class, several tests failed because they still expected an age parameter. Instead of assuming the code was correct, I reviewed the error messages, updated the tests to match the revised class definition, and reran pytest until all tests passed successfully.

---

## 4. Testing and Verification

### a. What you tested

I created automated tests for several important behaviors, including marking tasks as complete, adding tasks to pets, sorting tasks chronologically, generating recurring tasks for daily schedules, and detecting scheduling conflicts. These tests verify that the core scheduling logic works correctly and continues to function after future changes.

### b. Confidence

I am confident that the core scheduling system works correctly because all five automated tests pass, the command-line application produces the expected output, and the Streamlit interface successfully interacts with the backend classes. If I had more time, I would test additional edge cases such as invalid time formats, duplicate pet names, a very large number of pets and tasks, and overlapping recurring tasks across multiple days.

---

## 5. Reflection

### a. What went well

The part I am most satisfied with is building the scheduling system using object-oriented programming. Separating responsibilities into different classes made the application easier to understand, extend, and connect to the user interface.

### b. What you would improve

If I continued developing PawPal+, I would improve the user interface by making it more visually polished, adding calendar-based scheduling, allowing tasks to be edited directly, storing data in a database or JSON file, and supporting multiple owner accounts.

### c. Key takeaway

The biggest lesson I learned from this project is that spending time designing the system before writing code makes implementation much easier. I also learned that AI is most effective when used as a collaborative tool rather than simply copying its suggestions. Verifying AI-generated code with testing and debugging is an important part of the development process.