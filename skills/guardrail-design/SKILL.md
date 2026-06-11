---
name: guardrail-design
description: Design system guardrails, input validation rules, and UI fail-safes to protect non-technical users from destructive or irreversible actions. Trigger this skill on /guardrail-design and proactively whenever the user is designing an action that deletes, resets, or bulk-updates data, adding a settings or admin screen, designing a payment or submission flow, or any time someone says "what if the user accidentally clicks", "protect against mistakes", "add a confirmation", or "make it safe for non-technical users".
---

# Guardrail Design Skill (Protecting Non-Technical Users)

Ensure the system is designed to handle human errors, slipups, and accidents. A single accidental click must never result in catastrophic data loss, system-wide downtime, or irreversible state changes.

## Core Design Principles

You must incorporate the following safety patterns into system designs and codebases:

### 1. Multi-Step & Explicit Confirmations
For any destructive, irreversible, or high-risk actions (e.g., deleting a database record, clearing a cache, resetting configurations, bulk editing users):
- **Intentional Friction:** Never use simple one-click operations. Force the user to confirm via a second step (e.g., a modal dialog).
- **Match-Text Confirmation:** For extremely dangerous actions (such as deleting an entire project or database), require the user to explicitly type the name of the entity or a word (e.g., "DELETE") in a text input field to unlock the submit button.
- **Timed Actions:** In UI buttons, implement a "hold to confirm" pattern (requiring a mouse hold of 2–3 seconds) or a brief delayed countdown before execution begins.

### 2. The Undo Pattern & Soft Deletes
- **Soft Deletes by Default:** Do not execute hard destructive `DELETE` operations on primary database records. Implement a `deleted_at` (timestamp) field in your schema. Filter active queries to exclude soft-deleted rows.
- **Action Logs for Undo:** For major state mutations, store a transactional log of the action to support quick rollbacks (e.g., allowing a user to click an "Undo" toast notification within 10–15 seconds to reverse the change).

### 3. Strict Input Validation (Dual-Layer)
- **Frontend Masking & Hints:** Design UIs that restrict input errors at the source (e.g., date pickers, select dropdowns, input masks for phone/national IDs).
- **Hard Backend Schemas:** Never trust client-side validation. Enforce strict server-side schema validation on every API route (e.g., JSON Schema, Zod, class-validator, or framework-native options). Every string field must have a max-length constraint, every number must have min/max bounds, and enums must be tightly validated.

### 4. API Idempotency
- **Prevent Multi-Click Side Effects:** Design write-mutations (like payments, creations, or submissions) to accept an `Idempotency-Key` header. If a duplicate request is sent due to double-clicking, the server must return the cached response of the first transaction instead of executing a new one.

---

## Workflow Steps

You must follow these steps when designing or reviewing a feature under this skill:

### Step 1: High-Risk Action Identification
- Audit the proposed endpoints or features.
- Highlight any operations that delete data, perform bulk changes, update critical statuses, or modify billing/user roles.

### Step 2: Formulate Guardrails
- For each high-risk action identified, specify the guardrail pattern to be used:
  - Is it a Soft Delete?
  - Does it need a "Type to Confirm" UI modal?
  - Do we need backend idempotency key checks?
  - Do we need transaction rollbacks?
- Document these choices explicitly in `docs/system/architecture.md` or the corresponding `docs/backend/endpoints.md` / `docs/database/schema.md`.

### Step 3: Implement and Validate
- Write the schema validation rules first (route schema options, Zod schema, or middleware validators).
- Set up database columns (e.g., `deleted_at` column in a migration script).
- Write test cases verifying that invalid inputs are rejected, duplicate idempotent requests are safe, and soft deletes preserve raw records.
