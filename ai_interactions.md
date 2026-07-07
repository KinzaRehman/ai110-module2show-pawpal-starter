# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

### What task did you give the agent?

I asked the AI agent to help implement the PawPal+ application by generating the object-oriented class structure, improving the scheduling logic, integrating the backend with the Streamlit interface, and adding JSON persistence so pets and tasks would be saved between application runs.

### What did the agent do?

The agent:
- Generated the initial Owner, Pet, Task, Scheduler, and Plan classes.
- Suggested methods for sorting tasks, filtering tasks, detecting scheduling conflicts, and generating recurring tasks.
- Helped integrate the scheduling logic into the Streamlit application.
- Added JSON save/load functionality for persistent storage.
- Suggested improvements to the user interface layout and organization.

### What did you have to verify or fix manually?

I manually reviewed every suggested change before accepting it. I updated several unit tests after changing the `Pet` class constructor, corrected issues with recurring task behavior, refined the Streamlit layout and styling, verified that JSON persistence worked correctly, and reran the pytest suite after each major change to confirm that all tests continued to pass.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.
# AI Interactions Log

## Prompt Comparison (SF11)

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | ChatGPT (GPT-5.5) | ChatGPT (GPT-5.5) |
| **Prompt** | "Design the object-oriented architecture for PawPal+ using the required classes and implement the scheduling logic." | "Refactor the Streamlit application to create a cleaner, more user-friendly interface while preserving the existing backend functionality." |
| **Response summary** | Generated the Owner, Pet, Task, Scheduler, and Plan classes, along with scheduling algorithms such as sorting, filtering, conflict detection, recurring tasks, and JSON persistence. | Reorganized the Streamlit interface into grouped sections, improved spacing and layout, added styling, reorganized task management, and simplified the user workflow. |
| **What was useful** | Helped establish the overall object-oriented design and implement the required scheduling algorithms while keeping responsibilities separated across classes. | Improved the usability and readability of the application by grouping related information together and making the interface easier to navigate. |
| **Problems noticed** | Some generated code required manual updates after changes to the Pet class constructor caused existing unit tests to fail. JSON persistence also required additional testing to ensure data was saved and loaded correctly. | Some Streamlit styling behaved differently depending on the user's light or dark theme. Several layout and CSS changes required manual refinement and testing before the final interface behaved consistently. |
| **Decision** | Used as the foundation for the backend implementation after verifying functionality with pytest. | Adopted the improved interface while manually refining the final layout and verifying that the backend functionality continued to work correctly. |

### Which approach did you use in your final implementation and why?

I used both approaches together because they addressed different parts of the project. The first prompt focused on building the application's object-oriented architecture and scheduling logic, while the second focused on improving the overall user experience. After each change, I manually tested the application, verified the scheduling behavior using pytest, and confirmed that the Streamlit interface continued to interact correctly with the backend classes before accepting the changes.