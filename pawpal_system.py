from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents one pet care task."""
    title: str
    due_date: date
    due_time: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self):
        """Marks the task as completed."""
        self.completed = True

    def create_next_occurrence(self):
        """Creates the next recurring task if frequency is daily or weekly."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            title=self.title,
            due_date=next_date,
            due_time=self.due_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
        )
    

@dataclass
class Pet:
    """Represents a pet and the care tasks assigned to it."""
    name: str
    species: str
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a care task to the pet."""
        self.tasks.append(task)

    def list_tasks(self):
        """Returns all tasks for this pet."""
        return self.tasks

    def get_incomplete_tasks(self):
        """Returns only incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]
    

@dataclass
class Owner:
    """Represents a pet owner."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's collection."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Returns every task across all pets."""
        tasks = []

        for pet in self.pets:
            tasks.extend(pet.tasks)

        return tasks

class Scheduler:
    """Organizes, filters, and schedules tasks across all pets."""

    PRIORITY_ORDER = {
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    def __init__(self, owner: Owner):
        """Creates a scheduler for one owner."""
        self.owner = owner

    def get_all_tasks_with_pet(self):
        """Returns each task paired with the pet it belongs to."""
        all_tasks = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))

        return all_tasks

    def sort_by_time(self):
        """Returns all tasks sorted by due time."""
        return sorted(
            self.get_all_tasks_with_pet(),
            key=lambda pet_task: pet_task[1].due_time
        )

    def sort_by_priority_then_time(self):
        """Returns all tasks sorted by priority first, then time."""
        return sorted(
            self.get_all_tasks_with_pet(),
            key=lambda pet_task: (
                self.PRIORITY_ORDER.get(pet_task[1].priority, 2),
                pet_task[1].due_time
            )
        )

    def filter_by_pet(self, pet_name: str):
        """Returns tasks for one pet by name."""
        return [
            (pet, task)
            for pet, task in self.get_all_tasks_with_pet()
            if pet.name.lower() == pet_name.lower()
        ]

    def filter_by_status(self, completed: bool):
        """Returns tasks based on completion status."""
        return [
            (pet, task)
            for pet, task in self.get_all_tasks_with_pet()
            if task.completed == completed
        ]

    def detect_conflicts(self):
        """Finds tasks scheduled at the same date and time."""
        seen = {}
        conflicts = []

        for pet, task in self.get_all_tasks_with_pet():
            key = (task.due_date, task.due_time)

            if key in seen:
                conflicts.append((seen[key], (pet, task)))
            else:
                seen[key] = (pet, task)

        return conflicts

    def complete_task(self, pet_name: str, task_title: str):
        """Marks a task complete and creates next recurring task when needed."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                for task in pet.tasks:
                    if task.title.lower() == task_title.lower() and not task.completed:
                        task.mark_complete()

                        next_task = task.create_next_occurrence()
                        if next_task:
                            pet.add_task(next_task)

                        return task

        return None


@dataclass
class Plan:
    """Represents a generated care plan for the day."""
    owner_name: str
    scheduled_tasks: list

    def display(self):
        """Returns a readable schedule as text."""
        if not self.scheduled_tasks:
            return "No tasks scheduled."

        lines = [f"🐾 Daily Care Plan for {self.owner_name}"]

        for pet, task in self.scheduled_tasks:
            status = "✅ Done" if task.completed else "⏳ Pending"
            lines.append(
                f"{task.due_date} {task.due_time} | {pet.name} | {task.title} | "
                f"{task.priority.upper()} | {task.duration_minutes} min | {status}"
            )

        return "\n".join(lines)
    
