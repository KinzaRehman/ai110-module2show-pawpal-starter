import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler, Plan, save_owner_to_json, load_owner_from_json


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: #fff8f3; color: #263445; }
    .block-container { max-width: 1280px; padding-top: 1.25rem; padding-bottom: 2rem; }
    h1, h2, h3, h4 { color: #2f8f9d !important; }

    .hero { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
    .hero-left { display: flex; align-items: center; gap: 16px; }
    .hero-icon {
        width: 58px; height: 58px; border-radius: 18px; background: #ffe2dc;
        display: flex; align-items: center; justify-content: center; font-size: 32px;
    }
    .hero-title { font-size: 2.2rem; font-weight: 800; color: #2f8f9d; margin: 0; }
    .hero-subtitle { color: #667085; margin-top: 2px; font-size: 1rem; }
    .hero-avatar {
        width: 46px; height: 46px; border-radius: 50%; background: #ffd7cf;
        display: flex; align-items: center; justify-content: center; font-size: 22px;
    }

    .card {
        background: #ffffff; border: 1px solid #f0d8cc; border-radius: 22px;
        padding: 1.4rem 1.6rem; box-shadow: 0 12px 28px rgba(72, 64, 58, 0.07); margin-bottom: 18px;
    }
    .card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 0.15rem; }
    .card-icon {
        width: 40px; height: 40px; border-radius: 12px; background: #d9f0ee;
        display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0;
    }
    .card-icon.orange { background: #ffe3da; }
    .section-heading { font-size: 1.35rem; font-weight: 800; color: #2f8f9d; margin: 0; }
    .section-sub { color: #667085; margin: 4px 0 1.1rem 52px; }

    .pet-panel {
        background: #f5fbfb; border: 1px solid #cce9e8; border-radius: 18px;
        padding: 1rem 1.25rem; margin-top: 0.75rem;
    }
    .pet-row-label {
        background: #b8e7e4; color: #2f6f79; border-radius: 50%; width: 30px; height: 30px;
        display: inline-flex; align-items: center; justify-content: center; font-weight: 800; margin-top: 0.6rem;
    }
    .pet-emoji-badge {
        background: #f5fbfb; border: 1px solid #cce9e8; border-radius: 50%;
        width: 46px; height: 46px; display: flex; align-items: center; justify-content: center;
        font-size: 24px; margin-top: 0.15rem;
    }

    .tip {
        background: #eef9ef; border: 1px solid #cdeccd; color: #3b7f53;
        padding: 0.85rem 1rem; border-radius: 16px; margin-top: 0.75rem;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        background: #ffffff !important; color: #263445 !important;
        border: 1px solid #ead6cc !important; border-radius: 13px !important; min-height: 44px;
    }

    /* Closed selectbox control */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
        background: #ffffff !important; color: #263445 !important;
        border-color: #ead6cc !important; border-radius: 13px !important; min-height: 44px;
    }
    div[data-testid="stSelectbox"] * { color: #263445 !important; }
    div[data-testid="stSelectbox"] svg { fill: #263445 !important; }

    /* Open dropdown popover (rendered in a portal, outside .stApp) */
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] div[role="listbox"],
    ul[role="listbox"] {
        background: #ffffff !important; color: #263445 !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background: #f5fbfb !important; color: #263445 !important;
    }
    div[data-baseweb="popover"] * { color: #263445 !important; }

    label { color: #263445 !important; font-weight: 600 !important; }

    .stButton > button {
        background: linear-gradient(135deg, #f87676, #4aa3a8); color: white !important;
        border: none; border-radius: 14px; font-weight: 800; min-height: 44px; width: 100%;
        box-shadow: 0 8px 16px rgba(47, 143, 157, 0.18);
    }
    .stButton > button:hover { transform: translateY(-1px); color: white !important; }

    div[data-testid="stAlert"] { border-radius: 16px; }

    .task-table-header, .task-row {
        display: grid;
        grid-template-columns: 1.1fr 1.3fr 0.9fr 0.7fr 0.8fr 0.8fr 0.8fr 0.8fr 0.6fr;
        gap: 6px; align-items: center; padding: 8px 6px;
    }
    .task-table-header {
        background: #edf8f8; border-radius: 12px; color: #2f8f9d; font-weight: 800; font-size: 0.85rem;
    }
    .task-row { border-bottom: 1px solid #f2e8e0; font-size: 0.9rem; }
    .task-row:nth-child(even) { background: #fff8f1; }

    .badge {
        display: inline-block; padding: 3px 10px; border-radius: 999px; font-weight: 700; font-size: 0.78rem;
    }
    .badge-high { background: #ffe1e1; color: #c0392b; }
    .badge-medium { background: #ffedd5; color: #b5651d; }
    .badge-low { background: #e3f7e3; color: #2e7d32; }
    .badge-once { background: #eef1f8; color: #5763a3; }
    .badge-daily { background: #d9f0ee; color: #2f8f9d; }
    .badge-weekly { background: #ece3fb; color: #7248b5; }
    .badge-done { background: #e3f7e3; color: #2e7d32; }
    .badge-pending { background: #ffedd5; color: #b5651d; }

    .schedule-box {
        background: #ffffff; border: 1px solid #eadbd1; border-radius: 18px; padding: 1rem;
        font-family: monospace; white-space: pre-wrap; color: #263445;
    }
    .illustration { text-align: center; font-size: 70px; margin: 0.5rem 0 1rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-left">
            <div class="hero-icon">🐾</div>
            <div>
                <div class="hero-title">PawPal+</div>
                <div class="hero-subtitle">A calm pet care planner using OOP, scheduling logic, and Streamlit.</div>
            </div>
        </div>
        <div class="hero-avatar">👤</div>
    </div>
    """,
    unsafe_allow_html=True,
)

SPECIES_EMOJI = {"Cat": "🐱", "Dog": "🐶"}
TASK_EMOJI = {
    "Morning Walk": "🐾", "Medication": "💊", "Shower": "🛁", "Clip Nails": "✂️",
    "Feeding": "🍽️", "Vet Appointment": "🩺", "Other": "📌",
}
PRIORITY_BADGE = {"high": "badge-high", "medium": "badge-medium", "low": "badge-low"}
FREQ_BADGE = {"once": "badge-once", "daily": "badge-daily", "weekly": "badge-weekly"}


def species_emoji(species: str) -> str:
    return SPECIES_EMOJI.get(species, "🐾")


if "owner" not in st.session_state:
    st.session_state.owner = load_owner_from_json()

# ---------------------------------------------------------------- OWNER + PETS
# OWNER + PETS
st.markdown(
    """
    <div class="card" style="background:#FFF3EA; border:1px solid #F4CBB8;">
        <div class="section-heading">👤 Owner & Pets</div>
        <div class="section-sub">Add the owner, number of pets, pet names, and species in one place.</div>
    """,
    unsafe_allow_html=True,
)

owner_col, pets_col = st.columns([2, 1])

with owner_col:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

with pets_col:
    num_pets = st.number_input(
        "Number of pets",
        min_value=1,
        max_value=50,
        value=max(1, len(st.session_state.owner.pets) or 1),
    )

st.session_state.owner.name = owner_name

st.markdown(
    """
    <div style="
        background:#F4FBFA;
        border:1px solid #CDEBE8;
        border-radius:20px;
        padding:18px;
        margin-top:14px;
    ">
    """,
    unsafe_allow_html=True,
)

species_options = ["Cat", "Dog", "Other"]
pet_inputs = []

header = st.columns([0.5, 2, 2, 0.8])
with header[0]:
    st.markdown("**#**")
with header[1]:
    st.markdown("**Pet Name**")
with header[2]:
    st.markdown("**Species**")
with header[3]:
    st.markdown("**Icon**")

for i in range(num_pets):
    row = st.columns([0.5, 2, 2, 0.8])

    with row[0]:
        st.markdown(
            f"""
            <div style="
                background:#D8F0EE;
                color:#2F6F79;
                width:34px;
                height:34px;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:800;
                margin-top:8px;
            ">
                {i + 1}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with row[1]:
        default_name = (
            st.session_state.owner.pets[i].name
            if i < len(st.session_state.owner.pets)
            else f"Pet {i + 1}"
        )
        pet_name = st.text_input(
            "Pet name",
            value=default_name,
            key=f"pet_name_{i}",
            label_visibility="collapsed",
        )

    with row[2]:
        species_choice = st.selectbox(
            "Species",
            species_options,
            key=f"species_choice_{i}",
            label_visibility="collapsed",
        )

    with row[3]:
        pet_icon = "🐱" if species_choice == "Cat" else "🐶" if species_choice == "Dog" else "🐾"
        st.markdown(
            f"<div style='font-size:28px; text-align:center; margin-top:6px;'>{pet_icon}</div>",
            unsafe_allow_html=True,
        )

    if species_choice == "Other":
        custom_species = st.text_input(
            f"Enter species for Pet {i + 1}",
            key=f"custom_species_{i}",
        )
        species = custom_species
    else:
        species = species_choice

    pet_inputs.append((pet_name, species))

st.markdown("</div>", unsafe_allow_html=True)

save_col, note_col = st.columns([1, 3])

with save_col:
    save_pets = st.button("Save pets")

with note_col:
    st.markdown(
        """
        <div class="tip">
            🐾 Tip: Add as many pets as needed, then assign care tasks below.
        </div>
        """,
        unsafe_allow_html=True,
    )

if save_pets:
    st.session_state.owner.pets = []

    for pet_name, species in pet_inputs:
        if pet_name and species:
            st.session_state.owner.add_pet(Pet(pet_name, species))

    save_owner_to_json(st.session_state.owner)
    st.success("Pets saved!")

if st.session_state.owner.pets:
    pet_rows = [
        {"Pet Name": pet.name, "Species": pet.species}
        for pet in st.session_state.owner.pets
    ]
    st.table(pet_rows)
else:
    st.info("Enter pet information, then click Save pets.")

st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.owner.pets:
    st.stop()

# ---------------------------------------------------------- ADD TASK + CURRENT TASKS
left_card, right_card = st.columns([1, 1.35])

with left_card:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-header"><div class="card-icon orange">📝</div>'
        '<div class="section-heading">Add a Care Task</div></div>'
        '<div class="section-sub">Create a task and assign it to one pet.</div>',
        unsafe_allow_html=True,
    )

    selected_pet_name = st.selectbox("Choose pet", [pet.name for pet in st.session_state.owner.pets])

    task_options = list(TASK_EMOJI.keys())
    task_choice = st.selectbox(
        "Task title", task_options, format_func=lambda t: f"{TASK_EMOJI.get(t, '📌')} {t}",
    )

    if task_choice == "Other":
        task_title = st.text_input("Enter custom task")
    else:
        task_title = task_choice

    duration_options = [5, 10, 15, 20, 30, 45, 60, "Other"]
    duration_choice = st.selectbox(
        "Duration", duration_options,
        format_func=lambda x: f"{x} minutes" if isinstance(x, int) else x,
    )
    if duration_choice == "Other":
        duration = st.number_input("Enter custom duration", min_value=1, max_value=240, value=25)
    else:
        duration = duration_choice

    c1, c2 = st.columns(2)
    with c1:
        due_time = st.text_input("Due time HH:MM", value="09:00")
    with c2:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)

    selected_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)

    if st.button("+ Add task"):
        if task_title:
            task = Task(
                title=task_title,
                due_date=date.today(),
                due_time=due_time,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
            )
            selected_pet.add_task(task)
            save_owner_to_json(st.session_state.owner)
            st.success(f"Added {task_title} for {selected_pet.name}.")
        else:
            st.warning("Please enter a task title.")

    st.markdown("</div>", unsafe_allow_html=True)

with right_card:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-header"><div class="card-icon">📋</div>'
        '<div class="section-heading">Current Tasks</div></div>'
        '<div class="section-sub">Filter, review, and check off care tasks across pets.</div>',
        unsafe_allow_html=True,
    )

    scheduler = Scheduler(st.session_state.owner)

    filt_col1, filt_col2 = st.columns(2)
    with filt_col1:
        pet_filter = st.selectbox(
            "Filter by pet", ["All pets"] + [pet.name for pet in st.session_state.owner.pets],
        )
    with filt_col2:
        status_filter = st.selectbox("Filter by status", ["All", "Pending", "Done"])

    # Use the Scheduler's own filtering methods so tasks are actually
    # categorized/organized, not just listed.
    if pet_filter != "All pets":
        pairs = scheduler.filter_by_pet(pet_filter)
    else:
        pairs = scheduler.get_all_tasks_with_pet()

    if status_filter == "Pending":
        pending_ids = {id(t) for _, t in scheduler.filter_by_status(False)}
        pairs = [(p, t) for p, t in pairs if id(t) in pending_ids]
    elif status_filter == "Done":
        done_ids = {id(t) for _, t in scheduler.filter_by_status(True)}
        pairs = [(p, t) for p, t in pairs if id(t) in done_ids]

    pairs = sorted(pairs, key=lambda pt: pt[1].due_time)

    if pairs:
        st.markdown(
            '<div class="task-table-header">'
            '<div>Pet</div><div>Task</div><div>Date</div><div>Time</div>'
            '<div>Priority</div><div>Duration</div><div>Frequency</div><div>Status</div><div>Done</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        for pet, task in pairs:
            emoji = TASK_EMOJI.get(task.title, "🐾")
            prio_class = PRIORITY_BADGE.get(task.priority, "badge-medium")
            freq_class = FREQ_BADGE.get(task.frequency, "badge-once")
            status_class = "badge-done" if task.completed else "badge-pending"
            status_text = "Done" if task.completed else "Pending"

            row_cols = st.columns([1.1, 1.3, 0.9, 0.7, 0.8, 0.8, 0.8, 0.8, 0.6])
            row_cols[0].markdown(f"**{pet.name}**")
            row_cols[1].markdown(f"{emoji} {task.title}")
            row_cols[2].markdown(f"{task.due_date}")
            row_cols[3].markdown(f"{task.due_time}")
            row_cols[4].markdown(f'<span class="badge {prio_class}">{task.priority.title()}</span>', unsafe_allow_html=True)
            row_cols[5].markdown(f"{task.duration_minutes} min")
            row_cols[6].markdown(f'<span class="badge {freq_class}">{task.frequency.title()}</span>', unsafe_allow_html=True)
            row_cols[7].markdown(f'<span class="badge {status_class}">{status_text}</span>', unsafe_allow_html=True)

            checked = row_cols[8].checkbox(
                "Done", value=task.completed, key=f"done_{id(task)}", label_visibility="collapsed",
            )

            if checked and not task.completed:
                # Goes through the real Scheduler.complete_task so daily/weekly
                # tasks correctly spawn their next occurrence via
                # Task.create_next_occurrence().
                scheduler.complete_task(pet.name, task.title)
                save_owner_to_json(st.session_state.owner)
                st.rerun()
            elif not checked and task.completed:
                task.completed = False
                save_owner_to_json(st.session_state.owner)
                st.rerun()
    else:
        st.info("No tasks match this filter yet.")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------- BUILD SCHEDULE
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(
    '<div class="card-header"><div class="card-icon">🗓️</div>'
    '<div class="section-heading">Build Schedule</div></div>'
    '<div class="section-sub">Generate a priority-based plan and check for conflicts.</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="illustration">🐶💗🐱</div>', unsafe_allow_html=True)

scheduler = Scheduler(st.session_state.owner)

button_col, info_col = st.columns([1, 3])
with button_col:
    generate = st.button("Generate Schedule ✨")
with info_col:
    st.markdown(
        '<div class="tip">💡 High priority tasks are scheduled first, then by time. Conflicts are highlighted.</div>',
        unsafe_allow_html=True,
    )

if generate:
    scheduled_tasks = scheduler.sort_by_priority_then_time()
    plan = Plan(st.session_state.owner.name, scheduled_tasks)

    st.success("Schedule generated!")
    st.markdown(f'<div class="schedule-box">{plan.display()}</div>', unsafe_allow_html=True)

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning("Task conflict detected!")
        for first, second in conflicts:
            pet1, task1 = first
            pet2, task2 = second
            st.write(
                f"⚠️ {pet1.name}'s {task1.title} and "
                f"{pet2.name}'s {task2.title} are both at {task1.due_time}."
            )
    else:
        st.info("No conflicts found.")

st.markdown("</div>", unsafe_allow_html=True)

