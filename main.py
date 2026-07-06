from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler, Plan


owner = Owner(name="Kinza")

cat = Pet(name="Mochi", species="cat", age=2)
dog = Pet(name="Buddy", species="dog", age=4)

cat.add_task(Task("Breakfast", date.today(), "08:00", 15, "high", "daily"))
cat.add_task(Task("Medication", date.today(), "08:00", 5, "high", "daily"))
dog.add_task(Task("Evening Walk", date.today(), "18:30", 30, "medium", "daily"))
dog.add_task(Task("Grooming", date.today(), "13:00", 20, "low", "weekly"))

owner.add_pet(cat)
owner.add_pet(dog)

scheduler = Scheduler(owner)

print("\nTODAY'S SCHEDULE - SORTED BY PRIORITY THEN TIME")
plan = Plan(owner.name, scheduler.sort_by_priority_then_time())
print(plan.display())

print("\nCONFLICT WARNINGS")
conflicts = scheduler.detect_conflicts()

if conflicts:
    for first, second in conflicts:
        pet1, task1 = first
        pet2, task2 = second
        print(
            f"⚠️ Conflict: {pet1.name}'s {task1.title} and "
            f"{pet2.name}'s {task2.title} are both at {task1.due_time}."
        )
else:
    print("No conflicts found.")

print("\nMARKING BREAKFAST COMPLETE")
scheduler.complete_task("Mochi", "Breakfast")

updated_plan = Plan(owner.name, scheduler.sort_by_priority_then_time())
print(updated_plan.display())