---
name: self-evolution
description: Self-reflective loop that scans conversation history, extracts user corrections and execution errors, then rewrites the agent's own skill definitions to prevent those mistakes from recurring. Trigger on /self-evolution or [evolve-skills] and proactively when the user says "you keep making the same mistake", "update your rules", "learn from this", "fix your behavior", "remember this for next time", or after the user has corrected the same issue more than once in a session.
---

# Self-Evolution Skill (Self-Reflective Loop)

Enforce an automatic self-improvement cycle based on real feedback. Analyze conversation logs for model mistakes, direct user corrections, or execution failures, and update the rules in `SKILL.md` files dynamically to prevent recurring weaknesses.

---

## Core Invariants

You must strictly adhere to these safety rules during a self-evolution cycle:
1. **Focus on Specific Rules:** Do not write generic, vague statements. Write highly specific, actionable rules (e.g., "Must check index bounds before accessing...", "Do not use mock DB queries in route handlers").
2. **Do Not Break Base Behaviors:** Ensure the evolved rules do not conflict with the existing workflow steps (e.g., Design-First in `software-design`, or reproducing first in `debug-mantra`).
3. **Validate Registration:** After modifying any skill, always execute the listing/linking scripts to ensure the files parse correctly and remain active.
4. **Backup Before Modifying:** Before editing any `SKILL.md` file, copy its current contents to `scratch/skill-backup/<skill-name>_<timestamp>.md`. Never modify a skill file without a restorable backup existing first.
5. **Core Invariants Are Protected:** The `## Core Invariants` section of any skill is **read-only** during self-evolution. You are strictly forbidden from altering, removing, or weakening any item in a `Core Invariants` section without first presenting the proposed change to the user and receiving explicit written confirmation (e.g., user replies "confirmed" or "yes, change it").

---

## When NOT to Use
- Do NOT run `/self-evolution` mid-session while a debug or refactor task is still in progress — wait until the session reaches a natural conclusion.
- Do NOT use this skill to make cosmetic changes (wording tweaks, formatting) — it is reserved for substantive rule additions based on real observed failures.

---

## Workflow Steps

You must execute the self-evolution in this order. Do not skip any step:

### Step 1: Extract Feedback & Logs
Run the Python extraction script to compile a clean summary of the active conversation:
```powershell
python .\scripts\extract-feedback.py --app-data-dir "<app_data_dir>" --conv-id "<conversation_id>"
```
*Note: Replace `<app_data_dir>` and `<conversation_id>` with the values provided in the active session metadata.*

### Step 2: Read the Summary
Open and read the generated output file `scratch/feedback_summary.txt`. Look for:
- User corrections (e.g. user telling you to adjust your approach, fix formats, or prioritize a certain task).
- Error messages from tool execution status `ERROR` (e.g. command syntax failures, missing imports).
- Logic or syntax errors that you had to fix in code files.

### Step 3: Identify Weaknesses & Formulate Fixes
1. Classify the problems into distinct categories (e.g., "Code Quality", "Design-First violation", "Communication Style", "Error Handling").
2. Determine which skill file (`skills/<target-skill>/SKILL.md`) is responsible for this area.
3. Formulate specific instructions/rules to add to that skill file to prevent this mistake from happening again.

### Step 3.5: Backup Target Skill Files
Before writing any changes, copy the current content of each target skill file:
```powershell
# Example backup
Copy-Item skills\<target-skill>\SKILL.md scratch\skill-backup\<target-skill>_$(Get-Date -Format 'yyyyMMdd_HHmm').md
```
Confirm the backup file exists before proceeding.

### Step 4: Update the Target Skill(s)
- If the proposed change touches a `## Core Invariants` section: **STOP**. Show the user the exact line(s) to be changed and wait for explicit written confirmation before editing.
- Otherwise: use the file edit tools (`replace_file_content` or `multi_replace_file_content`) to update the target `skills/<target-skill>/SKILL.md` file. Add the new rules under the `Guidelines` or a new subsection — never inside `Core Invariants` without user approval.

### Step 5: Link & Verify
Run the linking and verification scripts in the workspace:
```powershell
.\scripts\link-skills.ps1
.\scripts\list-skills.ps1
```

### Step 6: Present Walkthrough
Report the results of the evolution to the user:
- **Mistakes/Weaknesses Detected:** Summarize what errors or user feedbacks were found in the log.
- **Evolved Skills:** Show the exact rules added and which `SKILL.md` files were modified.
- **Link & Verify status:** Confirm that the updated skills are compiled and active.
