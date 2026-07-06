from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task("Breakfast", date.today(), "08:00", 15, "high", "daily")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "cat")
    task = Task("Breakfast", date.today(), "08:00", 15)

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_sort_by_time_orders_tasks_chronologically():
    owner = Owner("Kinza")
    pet = Pet("Mochi", "cat")

    pet.add_task(Task("Dinner", date.today(), "18:00", 10))
    pet.add_task(Task("Breakfast", date.today(), "08:00", 10))

    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0][1].title == "Breakfast"
    assert sorted_tasks[1][1].title == "Dinner"


def test_daily_recurrence_creates_tomorrow_task():
    owner = Owner("Kinza")
    pet = Pet("Mochi", "cat")

    pet.add_task(Task("Breakfast", date.today(), "08:00", 15, frequency="daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.complete_task("Mochi", "Breakfast")

    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date > pet.tasks[0].due_date


def test_conflict_detection_finds_duplicate_time():
    owner = Owner("Kinza")
    pet = Pet("Mochi", "cat")

    pet.add_task(Task("Breakfast", date.today(), "08:00", 15))
    pet.add_task(Task("Medication", date.today(), "08:00", 5))

    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1