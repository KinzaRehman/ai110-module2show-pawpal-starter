"""
PawPal+ logic layer.
"""

import json
from datetime import date, datetime, timedelta
from typing import List, Tuple, Optional


PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


class Task:
    def __init__(self, title, due_date, due_time, duration_minutes,
                 priority="medium", frequency="once", completed=False):
        self.title = title
        self.due_date = due_date
        self.due_time = due_time
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.frequency = frequency
        self.completed = completed

    def mark_complete(self):
        self.completed = True

    def toggle_complete(self):
        self.completed = not self.completed

    def time_as_minutes(self):
        try:
            h, m = str(self.due_time).split(":")
            return int(h) * 60 + int(m)
        except Exception:
            return 0

    def create_next_occurrence(self):
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            self.title,
            next_date,
            self.due_time,
            self.duration_minutes,
            self.priority,
            self.frequency,
            False,
        )

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date.isoformat(),
            "due_time": self.due_time,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data["title"],
            due_date=date.fromisoformat(data["due_date"]),
            due_time=data["due_time"],
            duration_minutes=data["duration_minutes"],
            priority=data.get("priority", "medium"),
            frequency=data.get("frequency", "once"),
            completed=data.get("completed", False),
        )


class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)

    @property
    def task_count(self):
        return len(self.tasks)

    def to_dict(self):
        return {
            "name": self.name,
            "species": self.species,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @staticmethod
    def from_dict(data):
        pet = Pet(data["name"], data["species"])
        pet.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return pet


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def all_tasks(self):
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def to_dict(self):
        return {
            "name": self.name,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @staticmethod
    def from_dict(data):
        owner = Owner(data["name"])
        owner.pets = [Pet.from_dict(pet_data) for pet_data in data.get("pets", [])]
        return owner


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks_with_pet(self):
        pairs = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                pairs.append((pet, task))
        return pairs

    def filter_by_pet(self, pet_name):
        return [(p, t) for p, t in self.get_all_tasks_with_pet() if p.name == pet_name]

    def filter_by_status(self, completed):
        return [(p, t) for p, t in self.get_all_tasks_with_pet() if t.completed == completed]

    def sort_by_time(self):
        pairs = self.get_all_tasks_with_pet()
        pairs.sort(key=lambda pt: pt[1].time_as_minutes())
        return pairs

    def sort_by_priority_then_time(self):
        pairs = self.get_all_tasks_with_pet()
        pairs.sort(
            key=lambda pt: (
                PRIORITY_RANK.get(pt[1].priority, 1),
                pt[1].time_as_minutes(),
                pt[1].duration_minutes,
            )
        )
        return pairs

    def detect_conflicts(self):
        pairs = [pt for pt in self.get_all_tasks_with_pet() if not pt[1].completed]
        conflicts = []

        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                pet1, task1 = pairs[i]
                pet2, task2 = pairs[j]

                if task1.due_date == task2.due_date and task1.due_time == task2.due_time:
                    conflicts.append(((pet1, task1), (pet2, task2)))

        return conflicts

    def complete_task(self, pet_name, task_title):
        for pet in self.owner.pets:
            if pet.name != pet_name:
                continue

            for task in pet.tasks:
                if task.title == task_title and not task.completed:
                    task.mark_complete()
                    next_task = task.create_next_occurrence()

                    if next_task:
                        pet.add_task(next_task)

                    return next_task

        return None

    def next_available_slot(self, start_time="08:00", end_time="22:00", interval_minutes=15):
        """
        Bonus algorithm:
        Finds the next open time slot that does not already have a pending task.
        """
        occupied = {
            task.due_time
            for _, task in self.get_all_tasks_with_pet()
            if not task.completed and task.due_date == date.today()
        }

        current = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")

        while current <= end:
            slot = current.strftime("%H:%M")

            if slot not in occupied:
                return slot

            current += timedelta(minutes=interval_minutes)

        return None


class Plan:
    def __init__(self, owner_name, scheduled_tasks):
        self.owner_name = owner_name
        self.scheduled_tasks = scheduled_tasks

    def display(self):
        if not self.scheduled_tasks:
            return f"No tasks scheduled for {self.owner_name}."

        lines = [f"Schedule for {self.owner_name}", "=" * 42]

        for pet, task in self.scheduled_tasks:
            status = "DONE" if task.completed else "----"
            lines.append(
                f"[{status}] {task.due_date} {task.due_time} "
                f"({task.priority.upper():<6}) {pet.name} - {task.title} "
                f"({task.duration_minutes} min, {task.frequency})"
            )

        return "\n".join(lines)


def save_owner_to_json(owner, filename="data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(owner.to_dict(), file, indent=4)


def load_owner_from_json(filename="data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return Owner.from_dict(data)
    except FileNotFoundError:
        return Owner("Kinza")