---
name: code-refactoring
description: Restructure existing code to improve its internal design, readability, performance, or extensibility — without changing observable behavior. Trigger this skill on /code-refactoring and proactively whenever the user says "clean up", "too messy", "hard to read", "this is a mess", "spaghetti code", "pay down tech debt", "too complex", "too long", "extract this", "split this up", or pastes code and asks for feedback on structure — even if they never use the word "refactor".
---

# Code Refactoring Skill (Safe & Incremental Restructuring)

Always adopt a strict "Behavior-Preserving" stance. Refactoring is improving code quality without changing its observable external behavior. Do NOT introduce new features or fix unrelated bugs in the same refactoring cycle.

---

## Core Invariants

You must strictly adhere to these safety rules during any refactoring task:
1. **Separate Refactoring from Behavioral Changes:** Never mix new feature implementation or bug fixing with refactoring in the same block. Refactor first to make the change easy, then make the change.
2. **Incremental & Atomic Edits:** Make small, logical, self-contained changes. Do not attempt a massive multi-file rewrite at once. The codebase must be runnable at every single step.
3. **No Placeholders / Incomplete Logic:** Never leave `// TODO` stubs or deleted-code comments behind. Every file must be fully functional after the edit.
4. **Double-Ended Validation:** Run the test suite before you start (baseline) and immediately after every change (regression check).
5. **Visual Git Graph Required:** Whenever you perform any Git operation (like commit, checkout, or merge), you must always include a visual Git Graph diagram using a Markdown Mermaid block at the end of your response to show the current branch structure and commit history clearly.
6. **Never Merge Auth Middlewares:** During refactoring, you must **never** combine `verifyToken` (JWT) and `verifyApiKey` (API Key) into a single shared middleware or utility. They must remain completely separate modules. Merging them violates the core authentication design philosophy of this project.

---

## Before You Start

Run these three checks before touching a single line:

```bash
# 1. Confirm git working tree is clean — no uncommitted work
git status

# 2. Create a checkpoint so you can roll back to this exact state
git stash   # if changes exist
# — OR —
git commit -m "chore: checkpoint before refactor"

# 3. Confirm baseline tests pass at this commit
npm test    # or your project's test command
```

**After each atomic step:**
```bash
git diff          # review exactly what changed
npm test          # confirm no regression
git commit -m "refactor: <one-line description of what was extracted/moved/simplified>"
```

If a test fails after a step → `git stash` or `git checkout .` to revert that step, identify the behavioral divergence, and try again. Never accumulate uncommitted refactor changes across multiple steps.

---

## General Refactoring Principles

These patterns apply regardless of language or framework:

### 1. Thin Handler / Controller
Move business logic out of entry-point handlers into dedicated service or domain modules. Handlers should only: parse input → call service → return output.

**Before:**
```js
// ❌ Fat handler — validation, DB query, and business logic all tangled together
app.post('/users', async (req, reply) => {
  if (!req.body.email) throw new Error('email required')
  if (!req.body.email.includes('@')) throw new Error('invalid email')
  const existing = await db.query('SELECT id FROM users WHERE email = ?', [req.body.email])
  if (existing.length) throw new Error('duplicate')
  const user = await db.query('INSERT INTO users (email, created_at) VALUES (?, NOW())', [req.body.email])
  await mailer.send({ to: req.body.email, subject: 'Welcome' })
  return { id: user.insertId }
})
```

**After:**
```js
// ✅ Thin handler — delegates everything to a service
import { createUserSchema } from './schemas/user.schema.js'
import { userService } from './services/user.service.js'

app.post('/users', { schema: createUserSchema }, async (req, reply) => {
  return userService.create(req.body)
})
```

### 2. Extract Functions on Length or Complexity
Any function longer than ~30 lines or with a nesting depth > 3 is a candidate for extraction. Name each extracted function for what it *does*, not what it *is*.

### 3. Replace Raw Queries / Calls with Named Abstractions
Inline SQL strings, raw `fetch` calls, or repeated conditionals should be extracted into named query functions or helper modules so each call site is readable and the implementation is centralized.

### 4. Eliminate Duplication (DRY)
If the same logic appears in two or more places, extract it into a shared utility. Do not copy-paste fixes.

### 5. Validate at the Boundary, Trust Inside
Move input validation to the outermost layer (route schema, middleware, form validator). Inside the service layer, trust that inputs are already valid.

---

## Workflow Steps

You must execute refactoring in this order. Do not skip any step.

### Before You Start
Follow the git safety checklist above before touching any code.

### Step 1: Identify & Baseline
1. Identify the target files, functions, or queries to refactor.
2. Refer to the corresponding modular documentation file under `docs/` (`docs/system/architecture.md`, `docs/backend/endpoints.md`, `docs/frontend/components.md`, or `docs/database/schema.md`) to verify planned changes conform to the approved design. Do NOT scan the entire project.
3. Check for existing tests covering the target area. If none exist, write a minimal verification script (e.g., `scratch/verify.js`) to capture current input-to-output behavior.
4. Confirm the baseline passes.

### Step 2: Formulate the Refactoring Plan
1. Name the specific code smell (e.g., fat handler, duplicated logic, 3-level nesting, mixed concerns).
2. State the target structure and why it's better.
3. Break work into a numbered list of atomic steps — one extraction or move per step.

### Step 3: Execute Incrementally
1. Implement one atomic step.
2. Run `git diff` and then tests.
3. If tests pass: `git commit -m "refactor: ..."`. If tests fail: `git checkout .` and revisit.

### Step 4: Final Verification & Clean-up
1. Run full lint and static analysis.
2. Confirm no debug statements, broken imports, or orphaned files remain.
3. If performance was a goal, measure before/after (e.g., query count, response time).

### Step 5: Document the Improvement & Keep Docs In-Sync
- Show a concise **Before / After** comparison with code snippets.
- Report verification results (test output, lint clean).
- **CRITICAL INVARIANT:** Update the corresponding `docs/` file to reflect structural changes before declaring the task done.
