---
name: runbook-generator
description: Generate a short, zero-jargon operator guide (Runbook) in Thai/English for non-technical users, based on a completed bug fix or new feature. Trigger on /runbook-generator and proactively whenever a code change is merged or declared done, the user says "write the user guide", "document how to use this", "explain this to non-tech staff", "what do operators need to know", or after any feature or fix that changes a user-facing workflow.
---

# Runbook Generator Skill (Non-Technical Operator Guide)

Always adopt a strict "Zero-Jargon" stance. When a bug fix or new feature is completed, you must draft a short, clear "Runbook (คู่มือการใช้งานฉบับสั้น)" in plain, non-technical language (Thai/English) for the operator or end-user who runs the system daily.

---

## Core Invariants

You must strictly adhere to these rules when drafting a runbook:
1. **Absolute Zero-Jargon Rule:** Do NOT use code variables, database table names, SQL constraints, JSON payload keys, environment variables, or Fastify plugin names (e.g., do not write `users_db`, `PUT /api/v1/update`, or `user_id`). Use only UI terms (e.g., "ปุ่มสีเขียวเขียนว่า 'บันทึก'", "ช่องกรอกรหัสพนักงาน").
2. **Three Mandatory Pillars:** The guide must explicitly answer:
   - **ต้องกดปุ่มไหน (Which button to press):** The exact UI element, menu path, or button label to trigger the action.
   - **ใส่ค่าอะไร (What values to enter):** The exact inputs, selections, formats, or criteria required.
   - **ถ้าระบบขึ้นสีแดงต้องทำอย่างไร (What to do if system turns red/errors):** Actionable troubleshooting steps in user terms when errors occur.
3. **Keep it Concise:** Keep the guide short, under one page. Use bullet points and simple Markdown tables.

---

## Runbook Structure Template

Every runbook generated must follow this layout:

### [คู่มือการใช้งาน / Runbook] [ชื่อฟีเจอร์ หรือ บั๊กที่แก้ไข]

**รายละเอียดสั้น ๆ / Summary:**
- *[อธิบายภาษาไทยแบบคนทั่วไปเข้าใจว่าฟีเจอร์นี้ทำอะไร หรือบั๊กนี้แก้ปัญหาอะไร]*
- *[Plain English explanation of what this change does for the end-user]*

### ตารางการใช้งาน / Action Guide

| ขั้นตอน / Step | ต้องกดปุ่มไหน / Which button to press | ใส่ค่าอะไร / What values to enter |
| :--- | :--- | :--- |
| **1. [Step title]** | *[ระบุปุ่ม เมนู หรือสัญลักษณ์ที่จะกด]* / *[Specify the button, menu link, or icon to click]* | *[ระบุค่าที่ต้องกรอก หรือสิ่งที่ต้องเลือก]* / *[Specify values to fill or select]* |
| **2. [Step title]** | *[ระบุปุ่มยืนยัน]* / *[Specify submit/confirm button]* | *[ค่าอื่นๆ หรือปล่อยว่าง]* / *[Other inputs or leave empty]* |

### วิธีแก้ไขถ้าระบบขึ้นสีแดง / What to do if system turns red

| ข้อผิดพลาดที่เจอ (ขึ้นสีแดง) / Error Seen | สาเหตุ / Cause | วิธีแก้ไข / What to do |
| :--- | :--- | :--- |
| **[ข้อความแจ้งเตือนบนหน้าจอ]** | *[อธิบายสั้น ๆ]* / *[Short explanation]* | **[ขั้นตอนการแก้ไขของผู้ใช้]** / **[Actionable solution for user]** |
| **[ข้อความแจ้งเตือนบนหน้าจอ]** | *[อธิบายสั้น ๆ]* / *[Short explanation]* | **[ขั้นตอนการแก้ไขของผู้ใช้]** / **[Actionable solution for user]** |

---

## Workflow Steps

### Step 1: Scan Code Changes
- Read the git diff, PR details, or modified files in the codebase.
- Identify the UI inputs, buttons, database constraints, and user flows touched by the code change.

### Step 2: Extract Error Actions
- Read any caught database constraints, network errors, or Fastify validation schemas introduced.
- Look up the friendly translations mapped via the `jargon-free-error` skill.

### Step 3: Write the Runbook
- Generate the markdown document following the **Runbook Structure Template** above.
- Save the file under `docs/runbooks/runbook_<feature_name>.md`.
- Present a direct clickable link to the generated runbook to the user.
