# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

TODAY'S SCHEDULE - SORTED BY PRIORITY THEN TIME
🐾 Daily Care Plan for Kinza
2026-07-06 08:00 | Mochi | Breakfast | HIGH | 15 min | ⏳ Pending
2026-07-06 08:00 | Mochi | Medication | HIGH | 5 min | ⏳ Pending
2026-07-06 18:30 | Buddy | Evening Walk | MEDIUM | 30 min | ⏳ Pending
2026-07-06 13:00 | Buddy | Grooming | LOW | 20 min | ⏳ Pending

CONFLICT WARNINGS
⚠️ Conflict: Mochi's Breakfast and Mochi's Medication are both at 08:00.

MARKING BREAKFAST COMPLETE
🐾 Daily Care Plan for Kinza
2026-07-06 08:00 | Mochi | Breakfast | HIGH | 15 min | ✅ Done
2026-07-06 08:00 | Mochi | Medication | HIGH | 5 min | ⏳ Pending
2026-07-07 08:00 | Mochi | Breakfast | HIGH | 15 min | ⏳ Pending
2026-07-06 18:30 | Buddy | Evening Walk | MEDIUM | 30 min | ⏳ Pending
2026-07-06 13:00 | Buddy | Grooming | LOW | 20 min | ⏳ Pending

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:
======================================= test session starts =======================================

tests\test_pawpal.py ......                                                                  [100%]

======================================== 6 passed in 0.08s ========================================
```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` and `Scheduler.sort_by_priority_then_time()` | Tasks can be sorted chronologically or by priority first, then time. |
| Filtering | `Scheduler.filter_by_pet()` and `Scheduler.filter_by_status()` | The scheduler can show tasks for one pet or filter completed vs. incomplete tasks. |
| Conflict handling | `Scheduler.detect_conflicts()` | The app warns the owner when two tasks are scheduled for the same date and time. |
| Recurring tasks | `Task.create_next_occurrence()` and `Scheduler.complete_task()` | Daily tasks create a new task for the next day; weekly tasks create a new task for the next week. |

## 📸 Demo Walkthrough

1. Enter the owner's name and select how many pets you want to manage.
2. Enter each pet's name and species. Choose from Cat, Dog, or Other, and click **Save Pets** to store the information.
3. Select a pet and add one or more care tasks by choosing a task type (or entering a custom task), duration, due time, frequency, and priority.
4. View the current list of tasks for each pet in the task table. Tasks display the pet name, species, due date, due time, priority, duration, frequency, and completion status.
5. Click **Generate Schedule** to create the daily care plan. The Scheduler sorts tasks by priority and time, displays the schedule, and warns the user if any tasks are scheduled at the same date and time.
6. Run `main.py` to view the CLI demonstration, including recurring task generation after a task is marked complete.
7. Run `python -m pytest` to verify the application's core functionality through automated tests.

**Screenshot or video (optional):**

