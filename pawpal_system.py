"""
PawPal+ logic layer.

Contains the core domain classes (Task, Pet, Owner), the Scheduler
"brain" that organizes tasks across pets, and a Plan class used to
render a generated schedule.
"""

from datetime import timedelta
from typing import List, Tuple, Optional


PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


class Task:
    """A single pet-care activity (feeding, walk, medication, etc.)."""

    def __init__(self, title, due_date, due_time, duration_minutes,
                 priority="medium", frequency="once", completed=False):
        self.title = title
        self.due_date = due_date
        self.due_time = due_time            # string "HH:MM"
        self.duration_minutes = duration_minutes
        self.priority = priority            # "low" | "medium" | "high"
        self.frequency = frequency          # "once" | "daily" | "weekly"
        self.completed = completed

    def toggle_complete(self):
        """Flip the completed flag."""
        self.completed = not self.completed

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def time_as_minutes(self):
        """Convert 'HH:MM' due_time into total minutes for sorting."""
        try:
            h, m = str(self.due_time).split(":")
            return int(h) * 60 + int(m)
        except Exception:
            return 0

    def create_next_occurrence(self):
        """
        Build the next Task instance for recurring tasks.

        Daily tasks roll forward by 1 day, weekly tasks by 7 days.
        Returns None for one-off ("once") tasks, since they don't recur.
        """
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            title=self.title,
            due_date=next_date,
            due_time=self.due_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            completed=False,
        )


class Pet:
    """A pet belonging to an owner, holding its own list of tasks."""

    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Attach a new task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet, if present."""
        if task in self.tasks:
            self.tasks.remove(task)

    @property
    def task_count(self):
        """Number of tasks currently assigned to this pet."""
        return len(self.tasks)


class Owner:
    """The pet owner, who manages one or more pets."""

    def __init__(self, name):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> List[Task]:
        """Flatten every task across every pet into a single list."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    """The 'brain' that retrieves, organizes, sorts, and filters tasks
    across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks_with_pet(self) -> List[Tuple[Pet, Task]]:
        """Return every (pet, task) pair across the whole owner."""
        pairs = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                pairs.append((pet, task))
        return pairs

    def filter_by_pet(self, pet_name: str) -> List[Tuple[Pet, Task]]:
        """Return only the (pet, task) pairs belonging to the given pet."""
        return [(p, t) for p, t in self.get_all_tasks_with_pet() if p.name == pet_name]

    def filter_by_status(self, completed: bool) -> List[Tuple[Pet, Task]]:
        """Return only the (pet, task) pairs matching the completion status."""
        return [(p, t) for p, t in self.get_all_tasks_with_pet() if t.completed == completed]

    def sort_by_time(self) -> List[Tuple[Pet, Task]]:
        """Return all tasks sorted chronologically by due_time."""
        pairs = self.get_all_tasks_with_pet()
        pairs.sort(key=lambda pt: pt[1].time_as_minutes())
        return pairs

    def sort_by_priority_then_time(self) -> List[Tuple[Pet, Task]]:
        """Return all tasks sorted by priority (high first), then by time."""
        pairs = self.get_all_tasks_with_pet()
        pairs.sort(
            key=lambda pt: (
                PRIORITY_RANK.get(pt[1].priority, 1),
                pt[1].time_as_minutes(),
            )
        )
        return pairs

    def detect_conflicts(self):
        """
        Return a list of ((pet, task), (pet, task)) pairs where two
        *pending* tasks share the same due_date and due_time.
        Completed tasks are excluded since they no longer occupy a slot.
        """
        pairs = [pt for pt in self.get_all_tasks_with_pet() if not pt[1].completed]
        conflicts = []
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                pet1, task1 = pairs[i]
                pet2, task2 = pairs[j]
                if task1.due_date == task2.due_date and task1.due_time == task2.due_time:
                    conflicts.append(((pet1, task1), (pet2, task2)))
        return conflicts

    def complete_task(self, pet_name: str, task_title: str) -> Optional[Task]:
        """
        Mark the first pending task matching (pet_name, task_title) as
        complete. If it's a daily/weekly task, automatically spawn its
        next occurrence via Task.create_next_occurrence() and add it
        to the same pet. Returns the newly created task, or None.
        """
        for pet in self.owner.pets:
            if pet.name != pet_name:
                continue
            for task in pet.tasks:
                if task.title == task_title and not task.completed:
                    task.mark_complete()
                    next_task = task.create_next_occurrence()
                    if next_task is not None:
                        pet.add_task(next_task)
                    return next_task
        return None


class Plan:
    """A generated, display-ready schedule for an owner."""

    def __init__(self, owner_name, scheduled_tasks: List[Tuple[Pet, Task]]):
        self.owner_name = owner_name
        self.scheduled_tasks = scheduled_tasks

    def display(self) -> str:
        """Render the schedule as a readable, monospace-friendly string."""
        if not self.scheduled_tasks:
            return f"No tasks scheduled for {self.owner_name}."

        lines = [f"Schedule for {self.owner_name}", "=" * 42]
        for pet, task in self.scheduled_tasks:
            status = "DONE" if task.completed else "----"
            lines.append(
                f"[{status}] {task.due_time}  ({task.priority.upper():<6}) "
                f"{pet.name} - {task.title}  ({task.duration_minutes} min, {task.frequency})"
            )
        return "\n".join(lines)
